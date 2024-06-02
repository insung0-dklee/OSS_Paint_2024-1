import time  

class Timer:
    def __init__(self):
        self.start_time = None  
        self.elapsed_time = 0  
        self.running = False  

    def start(self):
        if not self.running:
            if self.start_time is None:
                self.start_time = time.time()  
            else:
                self.start_time = time.time() - self.elapsed_time
            self.running = True

    def get_elapsed_time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time  
        return self.elapsed_time

    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def add_time(self, seconds):
        self.elapsed_time += seconds
        if self.start_time is not None:
            self.start_time -= seconds

    def subtract_time(self, seconds):
        self.elapsed_time -= seconds
        if self.elapsed_time < 0:
            self.elapsed_time = 0
        if self.start_time is not None:
            self.start_time += seconds
            if self.start_time > time.time():
                self.start_time = time.time()    
"""
class timer 
@fun
    __init__(): 객체가 생성될 때 호출, 타이머 작동을 위해 변수를 초기화
    start():타이머가 현재 작동중인지 아닌지를 판별하고 만약 NONE이라면 현재 시간 저장
            그렇지 않은 경우 경과된 시간을 고려하여 시간 조정
    get_elapsed_time(): 현재 시간에서 시작시간을 뺀 경과시간 반환
    stop(): 타이머를 중지 
    add_time():매개변수인 seconds를 기존 타이머 경과시간에 추가하여 시간을 증가시킨다.
    subtract_time(): 매개변수인 seconds를 이용해 타이머 시간을 줄인다.시간에 음수는 없기 때문에
                    0보다 작을 경우 0으로 초기화 해주어 -를 방지한다.

"""
