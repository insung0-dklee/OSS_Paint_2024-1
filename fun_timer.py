import time  

class Timer:
    def __init__(self):
        self.start_time = None
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time if self.start_time is not None else time.time()
            self.running = True

    def get_elapsed_time(self):
        if self.running:
            return time.time() - self.start_time
        return self.elapsed_time

    def stop(self):
        if self.running:
            self.elapsed_time = self.get_elapsed_time()
            self.running = False
            return self.elapsed_time

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

"""
class timer
@fun
    __init__(): 객체가 생성될 때 호출, 타이머 작동을 위해 변수를 초기화
    start():타이머가 현재 작동중인지 아닌지를 판별하고 만약 NONE이라면 현재 시간 저장
            그렇지 않은 경우 경과된 시간을 고려하여 시간 조정
    get_elapsed_time(): 현재 시간에서 시작시간을 뺀 경과시간 반환
    stop(): 타이머를 중지
"""