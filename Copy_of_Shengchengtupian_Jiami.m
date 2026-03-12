function [IMG,time] = Copy_of_Shengchengtupian_Jiami(img11_RGB,img22_RGB)
t0=cputime;
tic
[m,n]=size(img11_RGB(:,:,1));
size1=m;


% permutations = perms(1:6); % 生成所有排列顺序
% numbers = 1:720; % 生成数字范围
% selected_permutations = zeros(720, 6); % 用于存储选择的排列顺序
% 
% 
% for i = 1:720
%     index = numbers(i);
%     selected_permutations(i, :) = permutations(index, :);
% end

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


shifted_1 = circshift(index_matrix, 1);  % 将向量 k 右移 6 位
shifted_2 = circshift(index_matrix, 2);  % 将向量 k 右移 6 位
shifted_3 = circshift(index_matrix, 3);  % 将向量 k 右移 6 位
shifted_4 = circshift(index_matrix, 4);  % 将向量 k 右移 6 位
shifted_5 = circshift(index_matrix, 5);  % 将向量 k 右移 6 位
shifted_6 = circshift(index_matrix, 6);  % 将向量 k 右移 6 位
selected_permutations = [shifted_1; shifted_2; shifted_3; shifted_4; shifted_5; shifted_6];



%六张图的六个参数
L1 = 6;
N0 = 1000;
q = zeros(1, L1);
xn=zeros(1, L1);

x1 =-0.8;
r1=0.9;
for i = 1:N0 + L1
    x1 = cos(r1 / asin(x1));
    if i > N0
        xn(i - N0) = x1;
        q(i - N0) = mod(floor(x1*10^15), m*m)+1;
    end
end


%扫描到六张图的每一个点都会进行重新排序
L2 = m*n;
M=zeros(1, L2);
N1 = 1000;
x2=0.8;
r2=1.2;
for i = 1:N1 + L2
    x2 = cos(r2 / asin(x2));
    if i > N1
        M(i - N1) = mod(floor(x2*10^15), 5)+1;
    end
end






%两轮的扫描置乱

%第一次置乱的状况

P11=New_saomiao_suijiQidian(q(1),img11_RGB (:,:,1),size1);
P22=New_saomiao_suijiQidian(q(2),img11_RGB (:,:,2),size1);
P33=New_saomiao_suijiQidian(q(3),img11_RGB (:,:,3),size1);
P44=New_saomiao_suijiQidian(q(4),img22_RGB (:,:,1),size1);
P55=New_saomiao_suijiQidian(q(5),img22_RGB (:,:,2),size1);
P66=New_saomiao_suijiQidian(q(6),img22_RGB (:,:,3),size1);



%汇总成6张512*512
Line_a=zeros(1,m*n*6);
for i=1:m*n
    
    Line_a(6*(i-1)+selected_permutations(M(i),1))=P11(i);
    Line_a(6*(i-1)+selected_permutations(M(i),2))=P22(i);
    Line_a(6*(i-1)+selected_permutations(M(i),3))=P33(i);
    Line_a(6*(i-1)+selected_permutations(M(i),4))=P44(i);
    Line_a(6*(i-1)+selected_permutations(M(i),5))=P55(i);
    Line_a(6*(i-1)+selected_permutations(M(i),6))=P66(i);

end



%裁剪回六张图
Line_img=reshape(Line_a,m,n*6);

Img_1_6=Line_img(:,1:n);
Img_2_6=Line_img(:,n+1:2*n);
Img_3_6=Line_img(:,2*n+1:3*n);
Img_4_6=Line_img(:,3*n+1:4*n);
Img_5_6=Line_img(:,4*n+1:5*n);
Img_6_6=Line_img(:,5*n+1:6*n);




%第二次置乱的状况

%扫描六个图像
P1_1_2=New_saomiao_suijiQidian(q(1),Img_1_6,size1);
P2_1_2=New_saomiao_suijiQidian(q(2),Img_2_6,size1);
P3_1_2=New_saomiao_suijiQidian(q(3),Img_3_6,size1);
P4_1_2=New_saomiao_suijiQidian(q(4),Img_4_6,size1);
P5_1_2=New_saomiao_suijiQidian(q(5),Img_5_6,size1);
P6_1_2=New_saomiao_suijiQidian(q(6),Img_6_6,size1);


%汇总成6张512*512
Line=zeros(1,m*n*6);
for i=1:m*n

    Line(6*(i-1)+selected_permutations(M(i),1))=P1_1_2(i);
    Line(6*(i-1)+selected_permutations(M(i),2))=P2_1_2(i);
    Line(6*(i-1)+selected_permutations(M(i),3))=P3_1_2(i);
    Line(6*(i-1)+selected_permutations(M(i),4))=P4_1_2(i);
    Line(6*(i-1)+selected_permutations(M(i),5))=P5_1_2(i);
    Line(6*(i-1)+selected_permutations(M(i),6))=P6_1_2(i);


end


%裁剪回六张图
Line_img_1=reshape(Line,m,n*6);  
Img_1=Line_img_1(:,1:n);
Img_2=Line_img_1(:,n+1:2*n);
Img_3=Line_img_1(:,2*n+1:3*n);
Img_4=Line_img_1(:,3*n+1:4*n);
Img_5=Line_img_1(:,4*n+1:5*n);
Img_6=Line_img_1(:,5*n+1:6*n);


%扩散
IMG=cat(6,Img_1,Img_2,Img_3,Img_4,Img_5,Img_6);



IMG1_before=horzcat(Img_1,Img_2,Img_3,Img_4,Img_5,Img_6);

IMG1_after=Function_anuode(IMG1_before);


IMG(:,:,1)=IMG1_after(:,1:n);
IMG(:,:,2)=IMG1_after(:,n+1:2*n);
IMG(:,:,3)=IMG1_after(:,n*2+1:3*n);
IMG(:,:,4)=IMG1_after(:,n*3+1:4*n);
IMG(:,:,5)=IMG1_after(:,n*4+1:5*n);
IMG(:,:,6)=IMG1_after(:,n*5+1:6*n);

IMG=uint8(IMG);

toc

end

