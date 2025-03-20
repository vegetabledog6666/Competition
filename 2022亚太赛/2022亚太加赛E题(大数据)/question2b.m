%% 数据处理
clc
clear
Data_test = readtable('2022_APMCM_E_Data.xlsx','Sheet', 'stockpiles');
Data_cell = table2cell(Data_test);
%国家标签转为数字编号
ContryLabel = Data_cell(:,1);
ContryLabel_cat = categorical(ContryLabel);
ContryLabel_int = double(ContryLabel_cat);
TotalContryNum = size(unique(ContryLabel_int),1);
[N,M] = size(Data_cell);

TotalYear = 78;
CountrysStocks = zeros(TotalContryNum+1,TotalYear);
for i= 1:N
    CountrysStocks(ContryLabel_int(i),Data_cell{i,3}-1944) = Data_cell{i,4};
end
for i=1:TotalYear
    CountrysStocks(TotalContryNum+1,i) = sum(CountrysStocks(1:TotalContryNum,i));
end
%% 预测全球核武数量
data = CountrysStocks(TotalContryNum+1,:)';
perVal = 24;
perLayer = 12;
perVal2 = [12,21,24,10,22,18,10,12,10,10];
perLayer2 = [8,10,10,10,10,10,10,10,10,10];
%% 模型训练
if ~exist('training_net2bgloabl.mat','file')
    net = MyTrainNet(data,perVal,perLayer);
    save('training_net2bgloabl.mat','net');
end
for i=1:TotalContryNum
    if ~exist(['training_net2b',num2str(i), '.mat' ],'file')
        data0 = CountrysStocks(i,1:78)';
        net2 = MyTrainNet(data0,perVal2(i),perLayer2(i));
        save(['training_net2b',num2str(i), '.mat' ],'net2');
    end
end

%% 预测
net = importdata('training_net2bgloabl.mat');
PreYear = 130-perVal;

[p,p2] = MyPerdict(net,data,perVal,PreYear);
p_conutry = zeros(TotalContryNum,length(p));
nets = cell(TotalContryNum,1);
for i=1:TotalContryNum
    net2 = importdata(['training_net2b',num2str(i), '.mat' ]);
    nets{i} = net2;
    data0 = CountrysStocks(i,:)';
    [pp,pp2] = MyPerdict(net2,data0,perVal,PreYear);
    p_conutry(i,:) = pp2;
end
len0 = length(data0);

for j=1:PreYear
    tempVal = zeros(TotalContryNum,1);
    for i = 1:TotalContryNum
        data2 = p_conutry(i,len0+j-perVal-1:len0+j-1);
        p3 = MyPerdict2(nets{i},data2,perVal);
        tempVal(i,1) = p3;
    end
    tempTotal = sum(tempVal);
    for i = 1:TotalContryNum
        p_conutry(i,len0 + j) = 0.25*tempVal(i,1)/tempTotal*p2(len0+j)+0.75*p_conutry(i,len0 + j);
    end
    
end


%% 绘图展示

figure(1)
X_p = [1945:1:2022];
X_p_2 = [1945:1:1945+length(p)-1];

for i=1:TotalContryNum
    subplot(2,5,i)
    Y_p = CountrysStocks(i,:);
    plot(X_p,Y_p,'r')
    hold on
    pp2 = p_conutry(i,:);
    plot(X_p_2,pp2,'b--');
    axis([min(X_p),max(X_p_2),0,max([max(Y_p),max(pp2)])]);
    xlabel('year');
    ylabel('stockpile');
    contrySTR = find(ContryLabel_int == i);
    legend({'真实值','预测值'});
    title(ContryLabel{contrySTR(1)})
end
figure(2)
Y_p = CountrysStocks(TotalContryNum+1,:);
plot(X_p,Y_p,'r')
hold on
plot(X_p_2,p2,'b--');
axis([min(X_p),max(X_p_2),0,max(p2)]);
xlabel('year');
ylabel('stockpile');
legend({'真实值','预测值'});
title('Global')






%% 函数
function net = MyTrainNet(data,perVal,perLayer)
    force=data;
    T=tonndata(force,false,false);  %输入和输出矩阵须为cell类型的矩阵，且不能用num2cell来转换，如果使用二维cell矩阵，将会被认为是两个输入从而不能训练?
    trainFcn = 'trainbr';   %默认的lmh函数训练时间序列效果很差，采用贝叶斯正则化算泿

    feedbackDelays = 1:perVal;    %延迟向量
    hiddenLayerSize = perLayer;
    net = narnet(feedbackDelays,hiddenLayerSize,'open',trainFcn);
    [Xs,Xi,Ai,Ts] = preparets(net,{},{},T);
    net.divideParam.trainRatio = 70/100;
    net.divideParam.valRatio = 15/100;
    net.divideParam.testRatio = 15/100;
    net = train(net,Xs,Ts,Xi,Ai);
    view(net);
end

function [p,p2] = MyPerdict(net,data,perVal,PreYear)
    len = length(data);    
    p = zeros(1,len+perVal);
    p2 = p;
    %前perVal个不预测直接用现成的
    p(1:perVal)= data(1:perVal);
    for i=1:len-perVal
        %依次用perVal个准确的预测下一丿
        ytest = num2cell(data(i:i + perVal)');
        [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);
        temp1 = net(AA,AB,AC);
        p(i+perVal) = temp1{1};
        p2(i+perVal) = round(p(i+perVal)*0.15 + data(i+perVal)*0.85);
    end
    %p2 = round(p);
    if PreYear>0
        for i=1:PreYear
            %迭代预测后续
            ytest = num2cell(p(len+i-perVal-1:len+i-1));
            [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);
            temp1 = net(AA,AB,AC);
            p(i+len) = temp1{1};
            p2(i+len) = ceil(p(i+len));
        end
    end
end

function p3 = MyPerdict2(net,data2,perVal)
    ytest = num2cell(data2);
    [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);
    temp1 = net(AA,AB,AC);
    p3 = ceil(temp1{1});
end
