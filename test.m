clear
r = 3.9;  % Logistic映射的参数
    x = 0.5 + 0.001 ;  % 初始值，稍微改变以生成不同的序列
    N = 6;  % 序列长度

    % 生成混沌序列
    chaotic_sequence = zeros(1, N);
    for i = 1:N
        x = r * x * (1 - x);
        chaotic_sequence(i) = x;
    end

    % 将混沌序列映射到1-512的整数范围
    mapped_sequence = round(1 + (N-1) * (chaotic_sequence - min(chaotic_sequence)) / (max(chaotic_sequence) - min(chaotic_sequence)));

    % 创建一个1-512的数组
    original_indices = 1:N;

    % 根据混沌序列进行排序，生成索引矩阵
    [~, sorted_indices] = sort(mapped_sequence);
    index_matrix = original_indices(sorted_indices);

    shifted_k = circshift(index_matrix, -1);  % 将向量 k 右移 6 位