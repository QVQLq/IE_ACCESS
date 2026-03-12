clear
img1=[1 2 3 4 5 6 ;  7 8 9 10 11 12 ; 13 14 15 16 17 18;19 20 21 22 23 24];

[m, n] = size(img1);
term2=3;
Line =New_Saomiao_2_changfangxing(term2, img1);
img1 = Decrypt_Saomiao_2_changfangxing(Line, m, n);
disp(Line)
disp(img1)


for
