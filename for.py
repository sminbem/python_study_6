def process_numbers():

    최종글=""
    for num in ["회사소개", "제품소개", "게시판"]:
        if num == "제품소개":
           
           continue
           
        최종글 += num
    
    return 최종글

# 함수 호출 및 결과 출력
result = process_numbers()
print("최종 반환된 값:", result)