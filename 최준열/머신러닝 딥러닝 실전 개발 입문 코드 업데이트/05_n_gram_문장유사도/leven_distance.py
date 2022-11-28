def calc_distance(a, b):
    '''레벤슈타인 거리 계산'''
    if a == b: return 0
    a_len = len(a)
    b_len = len(b)
    if a == "": return b_len # a 거리가 없으면 b 반환
    if b == "": return a_len
    
    # 2차원 표 준비(a_len+1, b_len+1)
    matrix = [[] for i in range(a_len+1)] # 행 생성
    for i in range(a_len+1):
        matrix[i] = [0 for j in range(b_len+1)] # 열 생성
    print("생성된 matrix: ", matrix)

    # 0일 때 초기값 생성
    for i in range(a_len+1): # 1열을 모두 0으로
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j

    # 표 채우기
    for i in range(1, a_len+1):
        ac = a[i-1]
        for j in range(1, b_len+1):
            bc = b[j-1]
            cost = 0 if (ac == bc) else 1 # 대각선 값을 0으로
            matrix[i][j] = min([
                matrix[i-1][j] + 1,     # 문자 삽입
                matrix[i][j-1] + 1,     # 문자 제거
                matrix[i-1][j-1] + cost # 문바 변경
                ])
    print("최종 matrix:", matrix)
    return matrix[a_len][b_len]

print(calc_distance("가나다라","가마바라"))

samples = ["신촌역", "신천군", "신천역", "신발", "마곡역"]
base = samples[0]
r = sorted(samples, key = lambda  n: calc_distance(base, n))
for n in r:
    print(calc_distance(base, n), n)

