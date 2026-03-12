function [img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG)

[m,n]=size(IMG(:,:,1));
size1=m;


permutations = perms(1:6); % 生成所有排列顺序
numbers = 1:720; % 生成数字范围
selected_permutations = zeros(720, 6); % 用于存储选择的排列顺序


for i = 1:720
    index = numbers(i);
    selected_permutations(i, :) = permutations(index, :);
end


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
L2 = size1*size1;
m=zeros(1, L2);
N1 = 1000;
x2=0.8;
r2=1.2;
for i = 1:N1 + L2
    x2 = cos(r2 / asin(x2));
    if i > N1
        m(i - N1) = mod(floor(x2*10^15), 719)+1;
    end
end



%扩散


IMG1_after(:,1:size1)=IMG(:,:,1);
IMG1_after(:,size1+1:2*size1)=IMG(:,:,2);
IMG1_after(:,size1*2+1:3*size1)=IMG(:,:,3);
IMG1_after(:,size1*3+1:4*size1)=IMG(:,:,4);
IMG1_after(:,size1*4+1:5*size1)=IMG(:,:,5);
IMG1_after(:,size1*5+1:6*size1)=IMG(:,:,6);


IMG1_before = Decrypt_Function_anuode(IMG1_after);


Img_1=IMG1_before(:,1:size1);
Img_2=IMG1_before(:,size1+1:2*size1);
Img_3=IMG1_before(:,2*size1+1:3*size1);
Img_4=IMG1_before(:,3*size1+1:4*size1);
Img_5=IMG1_before(:,4*size1+1:5*size1);
Img_6=IMG1_before(:,5*size1+1:6*size1);




%裁剪回六张图


Line_img_1(:,1:size1)=Img_1;
Line_img_1(:,size1+1:2*size1)=Img_2;
Line_img_1(:,2*size1+1:3*size1)=Img_3;
Line_img_1(:,3*size1+1:4*size1)=Img_4;
Line_img_1(:,4*size1+1:5*size1)=Img_5;
Line_img_1(:,5*size1+1:6*size1)=Img_6;



Line=reshape(Line_img_1,1,size1*size1*6);




P1_1_2=zeros(1,size1*size1);
P2_1_2=zeros(1,size1*size1);
P3_1_2=zeros(1,size1*size1);
P4_1_2=zeros(1,size1*size1);
P5_1_2=zeros(1,size1*size1);
P6_1_2=zeros(1,size1*size1);


%汇总成6张512*512
for i=1:size1*size1


    P1_1_2(i)=Line(6*(i-1)+selected_permutations(m(i),1));
    P2_1_2(i)=Line(6*(i-1)+selected_permutations(m(i),2));
    P3_1_2(i)=Line(6*(i-1)+selected_permutations(m(i),3));
    P4_1_2(i)=Line(6*(i-1)+selected_permutations(m(i),4));
    P5_1_2(i)=Line(6*(i-1)+selected_permutations(m(i),5));
    P6_1_2(i)=Line(6*(i-1)+selected_permutations(m(i),6));



end



%扫描六个图像
Img_1_6=New_saomiao_suijiQidian_Jiemi(q(1),P1_1_2,size1);
Img_2_6=New_saomiao_suijiQidian_Jiemi(q(2),P2_1_2,size1);
Img_3_6=New_saomiao_suijiQidian_Jiemi(q(3),P3_1_2,size1);
Img_4_6=New_saomiao_suijiQidian_Jiemi(q(4),P4_1_2,size1);
Img_5_6=New_saomiao_suijiQidian_Jiemi(q(5),P5_1_2,size1);
Img_6_6=New_saomiao_suijiQidian_Jiemi(q(6),P6_1_2,size1);




%裁剪回六张图

Line_img(:,1:size1)=Img_1_6;
Line_img(:,size1+1:2*size1)=Img_2_6;
Line_img(:,2*size1+1:3*size1)=Img_3_6;
Line_img(:,3*size1+1:4*size1)=Img_4_6;
Line_img(:,4*size1+1:5*size1)=Img_5_6;
Line_img(:,5*size1+1:6*size1)=Img_6_6;

Line_a=reshape(Line_img,1,size1*size1*6);



%汇总成6张512*512

P11=zeros(1,size1*size1);
P22=zeros(1,size1*size1);
P33=zeros(1,size1*size1);
P44=zeros(1,size1*size1);
P55=zeros(1,size1*size1);
P66=zeros(1,size1*size1);
for i=1:size1*size1


    P11(i)=Line_a(6*(i-1)+selected_permutations(m(i),1));
    P22(i)=Line_a(6*(i-1)+selected_permutations(m(i),2));
    P33(i)=Line_a(6*(i-1)+selected_permutations(m(i),3));
    P44(i)=Line_a(6*(i-1)+selected_permutations(m(i),4));
    P55(i)=Line_a(6*(i-1)+selected_permutations(m(i),5));
    P66(i)=Line_a(6*(i-1)+selected_permutations(m(i),6));



end




%恢复第一次置乱的状况
img11_RGB_b(:,:,1)=New_saomiao_suijiQidian_Jiemi(q(1),P11,size1);
img11_RGB_b(:,:,2)=New_saomiao_suijiQidian_Jiemi(q(2),P22,size1);
img11_RGB_b(:,:,3)=New_saomiao_suijiQidian_Jiemi(q(3),P33,size1);
img22_RGB_b(:,:,1)=New_saomiao_suijiQidian_Jiemi(q(4),P44,size1);
img22_RGB_b(:,:,2)=New_saomiao_suijiQidian_Jiemi(q(5),P55,size1);
img22_RGB_b(:,:,3)=New_saomiao_suijiQidian_Jiemi(q(6),P66,size1);

img11_RGB_b=uint8(img11_RGB_b);
img22_RGB_b=uint8(img22_RGB_b);

end

