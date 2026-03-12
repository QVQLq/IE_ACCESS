function r= ImCoef_function( A,N )
%选择N对来求相关性并画图

%r是向量，用来保存水平、垂直、正对角和反对角方向上的相关系数
A=double(A);   [m,n]=size(A); r=zeros(1,4);

x1=mod(floor(rand(1,N)*10^10),m-1)+1;
x2=mod(floor(rand(1,N)*10^10),m)+1;
x3=mod(floor(rand(1,N)*10^10),m-1)+2;
y1=mod(floor(rand(1,N)*10^10),n-1)+1;
y2=mod(floor(rand(1,N)*10^10),n)+1;

u1=zeros(1,N); u2=zeros(1,N); u3=zeros(1,N); u4=zeros(1,N);
v1=zeros(1,N); v2=zeros(1,N); v3=zeros(1,N); v4=zeros(1,N);
for i=1:N
    %u1和v1保存水平方向上的像素点对
    u1(i)=A(x1(i),y2(i)); v1(i)=A(x1(i)+1,y2(i));
    %u2和v2保存垂直方向上的像素点对
    u2(i)=A(x2(i),y1(i)); v2(i)=A(x2(i),y1(i)+1);
    %u3和v3保存正对角方向上的像素点对
    u3(i)=A(x1(i),y1(i)); v3(i)=A(x1(i)+1,y1(i)+1);
    %u4和v4保存反对角方向上的像素点对
    u4(i)=A(x3(i),y1(i)); v4(i)=A(x3(i)-1,y1(i)+1);
end
%调用计算公式计算相关系数,其中a.*b是将a矩阵与b矩阵中相同位置的元素相乘，两个矩阵的大小必须相等
r(1)=mean((u1-mean(u1)).*(v1-mean(v1)))/(std(u1,1)*std(v1,1));
r(2)=mean((u2-mean(u2)).*(v2-mean(v2)))/(std(u2,1)*std(v2,1));
r(3)=mean((u3-mean(u3)).*(v3-mean(v3)))/(std(u3,1)*std(v3,1));
r(4)=mean((u4-mean(u4)).*(v4-mean(v4)))/(std(u4,1)*std(v4,1));

%输出水平方向上随机选择的N对相邻像素点的相关图形，横坐标为u1的值，纵坐标为v1的值
%明文中相邻的像素值几乎相等，故由这两个相邻像素值所确定的位置在第一象限的对称位置
figure(101);
plot(u1,v1,'b.','linewidth',6,'markersize',6);  %线宽为3，MarkerSize——指定标识符的大小,k.表示黑色，r.表示红色
axis([0 300 0 300]);           %axis([xmin xmax ymin ymax]),设置坐标轴范围
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',18,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Vertical');  %水平

%输出垂直方向上随机选择的N对相邻像素点的相关图形，横坐标为u2的值，纵坐标为v2的值
figure(102);
plot(u2,v2,'b.','linewidth',6,'markersize',6);  %线宽为3，MarkerSize——指定标识符的大小,k.表示黑色，r.表示红色
axis([0 300 0 300]);           %axis([xmin xmax ymin ymax]),设置坐标轴范围
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',18,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
ylabel('Pixel gray value on location(\itx\rm,\ity\rm+1)');
title('Horizontal');  %垂直

%输出对角方向上随机选择的N对相邻像素点的相关图形，横坐标为u3的值，纵坐标为v3的值
figure(103);
plot(u3,v3,'b.','linewidth',6,'markersize',6);  %线宽为3，MarkerSize——指定标识符的大小,k.表示黑色，r.表示红色
axis([0 300 0 300]);           %axis([xmin xmax ymin ymax]),设置坐标轴范围
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',18,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm+1)');
title('Diagonal');  %对角

%输出垂直方向上随机选择的N对相邻像素点的相关图形，横坐标为u4的值，纵坐标为v4的值
figure(104);
plot(u4,v4,'b.','linewidth',6,'markersize',6);  %线宽为3，MarkerSize——指定标识符的大小,k.表示黑色，r.表示红色
axis([0 300 0 300]);           %axis([xmin xmax ymin ymax]),设置坐标轴范围
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',18,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
ylabel('Pixel gray value on location(\itx\rm-1,\ity\rm+1)');
title('Anti diagonal');  %反对角

end

