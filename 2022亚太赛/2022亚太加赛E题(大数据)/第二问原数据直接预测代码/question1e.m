%% 数据处理
clc
clear
Data_position = readtable("2022_APMCM_E_Data.xlsx",'Sheet', 'position');
Data_cell = table2cell(Data_position);
%将国家标签转为数字编号
ContryLabel = Data_cell(:,1);
ContryLabel_cat = categorical(ContryLabel);
ContryLabel_int = double(ContryLabel_cat);
TotalContryNum = size(unique(ContryLabel_int),1);
[N,M] = size(Data_cell);

%1938-2022,共85年
TotalYear = 85;
CountrysStatus = zeros(TotalContryNum,TotalYear);
for i= 1:N
    CountrysStatus(ContryLabel_int(i),Data_cell{i,3}-1937) = Data_cell{i,4};
end
count2 = 1;
for i=1:TotalContryNum
    st = max(CountrysStatus(i,:));
    if st>=3
        CountrysStatus2(count2,1) = i;
        CountrysStatus2(count2,2:86)=CountrysStatus(i,:);
        count2 = count2 + 1;
    end
end
%
%% 绘图
 figure(1)
X_p = [1938:1:2022];
for i=1:size(CountrysStatus2,1)
    subplot(2,5,i)
    Y_p = CountrysStatus2(i,2:86);
    plot(X_p,Y_p)
    axis([min(X_p),max(X_p),0,3]);
    xlabel('year');
    ylabel('state');
    contrySTR = find(ContryLabel_int == CountrysStatus2(i,1));
    
    title(ContryLabel{contrySTR(1)})
end


