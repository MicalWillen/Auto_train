import os
import time
import shutil
from threading import Thread, Event

import FormatOperation
import TriggerPDCA

class MonitorThread(Thread):
    def __init__(self, pathroot, dataGridView1):
        super().__init__()
        self.pathroot = pathroot
        self.fo = FormatOperation.FormatOperationer()
        self.m_pdca = TriggerPDCA.PDCA()
        self.dataGridView1 = dataGridView1
        self.isrunning = False  # 默认不运行
        self.stop_event = Event()  # 用于控制线程停止
        self.daemon = True  # 设为守护线程，确保主线程退出时它也能退出

    def run(self):
        """线程主循环"""
        while not self.stop_event.is_set():  # 线程存活时循环运行
            if not self.isrunning:
                time.sleep(1)  # 休眠等待，减少 CPU 占用
                continue

            # 清空数据缓存
            self.fo.clear_send_msg()
            self.fo.clear_pdca_name()
            self.fo.clear_data_output()

            # 获取目录中的文件列表
            file_list = [f for f in os.listdir(self.pathroot) if os.path.isfile(os.path.join(self.pathroot, f))]
            if not file_list:  # 目录为空，继续等待
                time.sleep(1)
                continue

            # 连接 PDCA 服务器
            self.m_pdca.connect("PDCA")

            # 处理文件
            file_path = os.path.join(self.pathroot, file_list[0])
            f = os.path.basename(file_path)
            self.fo.ReadOutputData(50, 97, file_path, self.fo.data_outputs)

            for m in range(0, len(self.fo.data_outputs), 2):
                temp_onepcs = [self.fo.data_outputs[m], self.fo.data_outputs[m + 1]]

                # 解析数据
                self.fo.ReflectionDataSheet(temp_onepcs, self.fo.dynamic_list, self.fo.sendmsg, 
                                             self.fo.PDCA_Name, self.fo.output_Data)

                # 获取序列号（SN）
                temp_sendmsg = self.fo.sendmsg.split(',')
                current_sn = temp_sendmsg[0].split(':')[1].split(' ')[0].strip('"')

                sendres = ""
                linend_token = "@90@120@degrees\n"  # 行尾标记

                # 组装 PDCA 发送数据
                for k in range(1, len(temp_sendmsg)):
                    if temp_sendmsg[k]:
                        # sendres += f"{current_sn}@pdata@{temp_sendmsg[k].split(':')[0]}@" \
                        #            f"{temp_sendmsg[k].split(':')[1].strip('\"')}"+linend_token
                        sendres="1"

                # 组装最终发送消息
                sendmsg = f"_{{\n{current_sn}@start\n{sendres}{current_sn}@pdata@Mode@0\n" \
                          f"{current_sn}@submit@WCA-XX.XX-XX.XX-XX.XX\n}}\n"

                # 更新 UI 界面
                temp_list = [self.fo.PDCA_Name, self.fo.output_Data]
                self.dataGridView1.Invoke(lambda: self.fo.ReadParaCSV(self.dataGridView1, temp_list, True))

                # 处理文件移动
                done_dir = os.path.join(self.pathroot, "Done")
                os.makedirs(done_dir, exist_ok=True)
                done_file_path = os.path.join(done_dir, f)
                if os.path.exists(done_file_path):
                    os.remove(done_file_path)
                shutil.move(file_path, done_file_path)

                # 发送数据到 PDCA 服务器
                self.m_pdca.Send_Msg_By_Client(sendmsg)
                self.m_pdca.Recv_Msg_By_Client()

                # 检查 PDCA 服务器返回的状态
                if "ok" not in self.m_pdca.now_PDCAStatus:
                    print(f"{current_sn} upload failed...")

            # 关闭 PDCA 连接
            self.m_pdca.Close()

    def stop(self):
        """完全停止线程"""
        self.stop_event.set()
