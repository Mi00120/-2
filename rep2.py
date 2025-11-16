import sys

def print_matrix(matrix, title="행렬", n=5):
    print(f"\n--- {title} ---")
    if not matrix:
        print(" (행렬이 비어있습니다)")
        return
    if len(matrix) < n:
        print(" (행렬의 행 수가 부족합니다)")
        return

    for i in range(n):

        if len(matrix[i]) < n:
            print(f" ( {i+1}번째 행의 열 수가 부족합니다)")

            for j in range(len(matrix[i])):
                print(int(matrix[i][j]), end=" ")
            for j in range(len(matrix[i]), n):
                print("?", end=" ")
            print()
            continue

        for j in range(n):
            print(int(matrix[i][j]), end=" ")
        print()

def get_matrix(n=5):
    matrix = []
    print(f"집합 A = {{1, 2, 3, 4, 5}} 에 대한 {n}x{n} 관계 행렬을 입력합니다.")
    print("각 행의 원소를 공백으로 구분하거나 붙여서 5개씩 입력하세요 (0 또는 1).")

    for i in range(n):
        while True:
            try:
                row_input = input(f"{i + 1}번째 행 입력: ")
                processed_input = row_input.replace(" ", "")

                if not processed_input.isdigit():
                    print(f"오류: 0 또는 1로 구성된 숫자만 입력해야 합니다. 다시 입력해주세요.")
                    continue

                row = [int(char) for char in processed_input]

                if len(row) != n:
                    print(f"오류: 정확히 {n}개의 원소를 입력해야 합니다. 다시 입력해주세요.")
                    continue

                matrix.append(row)
                break
            except ValueError:
                print("오류: 유효하지 않은 입력입니다. 다시 입력해주세요.")
                continue

    return matrix

def is_reflexive(matrix, n=5):
    for i in range(n):
        if matrix[i][i] == 0:
            return False
    return True

def is_symmetric(matrix, n=5):
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

def is_transitive(matrix, n=5):
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix[i][j] == 1 and matrix[j][k] == 1:
                    if matrix[i][k] == 0:
                        return False
    return True

def check_relation_properties(matrix, n=5, title="관계 R"):
    print(f"\n--- [ {title} ]의 성질 판별 ---")

    reflexive = is_reflexive(matrix, n)
    symmetric = is_symmetric(matrix, n)
    transitive = is_transitive(matrix, n)

    print(f"1. 반사 관계 (Reflexive): {'O' if reflexive else 'X'}")
    print(f"2. 대칭 관계 (Symmetric): {'O' if symmetric else 'X'}")
    print(f"3. 추이 관계 (Transitive): {'O' if transitive else 'X'}")

    if reflexive and symmetric and transitive:
        print(f"\n[결과] {title}은(는) 동치 관계(Equivalence Relation)입니다.")
        return True
    else:
        print(f"\n[결과] {title}은(는) 동치 관계가 아닙니다.")
        return False

def find_equivalence_classes(matrix, n=5):
    print("\n--- 동치류 (Equivalence Classes) ---")
    elements = list(range(1, n + 1))
    visited = [False] * n

    for i in range(n):
        if not visited[i]:
            current_class = []
            for j in range(n):
                if matrix[i][j] == 1:
                    current_class.append(elements[j])
                    visited[j] = True

            print(f"원소 {elements[i]}의 동치류 [{elements[i]}]: {sorted(current_class)}")

def get_reflexive_closure(matrix, n=5):
    closure = [row[:] for row in matrix]
    for i in range(n):
        closure[i][i] = 1
    return closure

def get_symmetric_closure(matrix, n=5):
    closure = [row[:] for row in matrix]
    for i in range(n):
        for j in range(i + 1, n):
            if closure[i][j] == 1 or closure[j][i] == 1:
                closure[i][j] = 1
                closure[j][i] = 1
    return closure

def get_transitive_closure(matrix, n=5):
    closure = [row[:] for row in matrix]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
                closure[i][j] = int(closure[i][j])

    return closure

def main():
    n = 5

    original_matrix = get_matrix(n)
    print_matrix(original_matrix, "입력된 관계 행렬 (R)")

    is_equivalence = check_relation_properties(original_matrix, n, "초기 관계 R")

    if is_equivalence:
        find_equivalence_classes(original_matrix, n)

    else:
        print("\n" + "="*30)
        print("동치 관계가 아니므로, 폐포 계산을 시작합니다.")
        print("="*30)

        print("\n[단계 1] 개별 폐포 계산")

        r_closure = get_reflexive_closure(original_matrix, n)
        print_matrix(original_matrix, "변환 전 (R)")
        print_matrix(r_closure, "반사 폐포 (r(R))")

        s_closure = get_symmetric_closure(original_matrix, n)
        print_matrix(original_matrix, "변환 전 (R)")
        print_matrix(s_closure, "대칭 폐포 (s(R))")

        t_closure = get_transitive_closure(original_matrix, n)
        print_matrix(original_matrix, "변환 전 (R)")
        print_matrix(t_closure, "추이 폐포 (t(R))")

        print("\n[단계 2] 동치 폐포(Equivalence Closure) 계산 및 재판별")
        print("동치 폐포는 t(s(r(R))) 순서로 계산합니다.")

        closure_step1 = get_reflexive_closure(original_matrix, n)
        closure_step2 = get_symmetric_closure(closure_step1, n)
        equivalence_closure = get_transitive_closure(closure_step2, n)

        print_matrix(equivalence_closure, "최종 동치 폐포 (t(s(r(R))))")

        final_is_equivalence = check_relation_properties(equivalence_closure, n, "동치 폐포")

        if final_is_equivalence:
            find_equivalence_classes(equivalence_closure, n)
        else:
            print("오류: 동치 폐포가 동치 관계가 아닙니다. 로직을 확인하세요.")

if __name__ == "__main__":
    main()
