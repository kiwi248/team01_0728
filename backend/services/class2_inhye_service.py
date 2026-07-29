from backend.schemas.class2_inhye_schema import Student2Public

# 1. 입력
def Student2_create(product:Student2Public) -> Student2Public:
    print("Database 에 입력이 처리 됩니다....")
    return product

# 2. 전체조회
def Student2_get_all() -> list[Student2Public]:
    result = [];

    result.append(Student2Public(id=1, name = "사람1", Korean =58,English=70,Math=80))
    result.append(Student2Public(id=2, name = "사람2", Korean =98,English=50,Math=68))
    result.append(Student2Public(id=3, name = "사람3", Korean =89,English=40,Math=89))
    result.append(Student2Public(id=4, name = "사람4", Korean =53,English=56,Math=90))
    result.append(Student2Public(id=5, name = "사람5", Korean =80,English=55,Math=70))
    result.append(Student2Public(id=6, name = "사람6", Korean =29,English=66,Math=68))
    result.append(Student2Public(id=7, name = "사람7", Korean =96,English=76,Math=45))
    result.append(Student2Public(id=8, name = "사람8", Korean =58,English=77,Math=76))
    result.append(Student2Public(id=9, name = "사람9", Korean =69,English=88,Math=57))
    result.append(Student2Public(id=10, name = "사람10", Korean =99,English=99,Math=78))
  
    return result 