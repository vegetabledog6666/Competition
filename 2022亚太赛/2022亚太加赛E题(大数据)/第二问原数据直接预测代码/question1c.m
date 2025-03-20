%% 数据处理
clc
clear
Data_test = readtable("2022_APMCM_E_Data.xlsx",'Sheet', 'tests');
Data_cell = table2cell(Data_test);
%国家标签转为数字编号
ContryLabel = Data_cell(:,1);
ContryLabel_cat = categorical(ContryLabel);
ContryLabel_int = double(ContryLabel_cat);
TotalContryNum = size(unique(ContryLabel_int),1);
[N,M] = size(Data_cell);
TotalYear = 75;
year_test = zeros(TotalYear,3);
%遍历国家，统计每年核试验次数
for i = 1:TotalContryNum
    for j = 1:TotalYear
        year_test(j,1) = 1944+j;
        year_test(j,2) = year_test(j,2) + Data_cell{(i-1)*TotalYear+j,4};
    end
end
%累加5年总次数
for i=5:TotalYear
    year_test(i,3) = sum(year_test(i-4:i,2));
end


%% 绘图展示
figure(1)
X_p = year_test(:,1)';
Y_p = year_test(:,2)';
Z_p = year_test(:,3)';
plot(X_p,Y_p,'g-','linewidth',1)
hold on
plot(X_p,Z_p,'r-','linewidth',1)

axis([min(X_p),max(X_p),0,max(Z_p)]);
xlabel('year','FontSize',15);
ylabel('test','Fontsize',15);
title('Global Nuclear Test Times')
