permutations = perms(1:6); % 生成所有排列顺序
numbers = 1:720; % 生成数字范围
selected_permutations = zeros(720, 6); % 用于存储选择的排列顺序


for i = 1:720
    index = numbers(i);
    selected_permutations(i, :) = permutations(index, :);
end