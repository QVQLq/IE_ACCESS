function [IMG] = Shengchengtupian_Jiami_gai(IMG,q,m,size1)

img11 = IMG(:,:,1);
img22 = IMG(:,:,2);
img33 = IMG(:,:,3);
img44 = IMG(:,:,4);
img55 = IMG(:,:,5);
img66 = IMG(:,:,6);


permutations = perms(1:6); % 生成所有排列顺序
numbers = 1:720; % 生成数字范围
selected_permutations = zeros(720, 6); % 用于存储选择的排列顺序


for i = 1:720
    index = numbers(i);
    selected_permutations(i, :) = permutations(index, :);
end



%两轮的扫描置乱

%第一次置乱的状况

P1_1_1=New_saomiao_suijiQidian(q(1),img11,size1);
P2_1_1=New_saomiao_suijiQidian(q(2),img22,size1);
P3_1_1=New_saomiao_suijiQidian(q(3),img33,size1);
P4_1_1=New_saomiao_suijiQidian(q(4),img44,size1);
P5_1_1=New_saomiao_suijiQidian(q(5),img55,size1);
P6_1_1=New_saomiao_suijiQidian(q(6),img66,size1);



%汇总成6张512*512
Line_a=zeros(1,size1*size1*6);
for i=1:size1*size1
    
    Line_a(6*(i-1)+selected_permutations(m(i),1))=P1_1_1(i);
    Line_a(6*(i-1)+selected_permutations(m(i),2))=P2_1_1(i);
    Line_a(6*(i-1)+selected_permutations(m(i),3))=P3_1_1(i);
    Line_a(6*(i-1)+selected_permutations(m(i),4))=P4_1_1(i);
    Line_a(6*(i-1)+selected_permutations(m(i),5))=P5_1_1(i);
    Line_a(6*(i-1)+selected_permutations(m(i),6))=P6_1_1(i);

end



%裁剪回六张图
Line_img=reshape(Line_a,size1,size1*6);

IMG(:,:,1)=Line_img(:,1:size1);
IMG(:,:,2)=Line_img(:,size1+1:2*size1);
IMG(:,:,3)=Line_img(:,2*size1+1:3*size1);
IMG(:,:,4)=Line_img(:,3*size1+1:4*size1);
IMG(:,:,5)=Line_img(:,4*size1+1:5*size1);
IMG(:,:,6)=Line_img(:,5*size1+1:6*size1);


IMG=uint8(IMG);


end