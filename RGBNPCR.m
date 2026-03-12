
IMG1=Shengchengtupian_Jiami(img);
n=100;
NPCR_sum=0;
UACI_sum=0;

for k=1:n

 img_change= change_one_pixel(img_change);
 IMG2=Shengchengtupian_Jiami(img_change);



%连成512*（512*6）的Horz_1和Horz_2
Horz_1=horzcat(IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3));
Horz_2=horzcat(IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3));


%检测其NPCR,UACI
[NPCR,UACI] = function_NPCRUACI(Horz_1, Horz_2) ;


disp(NPCR)
disp(UACI)
NPCR_sum=NPCR+NPCR_sum;
UACI_sum=UACI+UACI_sum;


end
NPCR_ave=double(NPCR_sum/n);
UACI_ave=double(UACI_sum/n);
fprintf('NPCR:%f,UACI:%f\n',NPCR_ave,UACI_ave);