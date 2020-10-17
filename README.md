# Báo cáo P2

## Q1
python pacman.py --frameTime 0 -p ReflexAgent -k 1

* Hướng làm:

    Ý tưởng nâng cấp hàm evaluationFunction(): sử dụng manhattan tính khoảng cách đến đồ ăn, làm tham số để tính điểm của hàm đánh giá.
	và tính toán khoảng các đến đồ ăn và trả về giá trị min.

## Q2
python pacman.py --frameTime 0 -p ReflexAgent -k 2

* Hướng làm:

    Ý tưởng nâng cấp hàm getAction(): với độ sâu cho trước lần lượt thực hiện findMax với Pacman và findMin với các con ma, độ sau chỉ cập nhật khi chuyển từ findMax sang findMin hoặc ngược lại.

    Sau khi tính toán sẽ nhận được mảng gồm các actions và điểm cho action đó, dựa vào đó ta chọ action tốt nhất và trả về.

## Q3
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4

* Hướng làm:

    Ý tưởng nâng cấp hàm getAction(): tương tự như ở Q3 nhưng thêm phần cập nhật giá trị alpha và beta, có thể hiểu là điểm số tốt nhất của hành động đối với pacman và với những con ma.

    Phần chọn hành động tối ưu vẫn dựa trên giá trị trả về tương tự câu trên.

## Q4
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic

* Hướng làm:

    Ý tưởng nâng cấp hàm getAction(): tương tự AlphaBetaAgent tuy nhiên thay hàm findMin tìm giá trị nhỏ nhất bằng hàm findAvg trong hàm đó giá trị value trả về là tổng các giá trị của từng con ma nhân với xác suất của nó.

    Phần chọn hành động tối ưu vẫn dựa trên giá trị trả về tương tự câu trên.

## Q5
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10

* Hướng làm:

    Ý tưởng nâng cấp hàm betterEvaluationFunction(): tương tự ý tưởng nâng cấp hàm evaluationFunction() nhưng thay vì dùng giá trị -1 và 1 ta dùng -inf và inf ùng với đó là tính toán giá trị dựa trên khoảng cách đến thức ăn gần nhất, ma gần nhất và mà xa nhất cùng với các trọng số thích hợp.
