%% 数据处理
clc
clear
Data_test = readtable('2022_APMCM_E_Data.xlsx','Sheet', 'stockpiles');
Data_cell = table2cell(Data_test);
%国家标签转为数字编号
ContryLabel = Data_cell(:,1);
ContryLabel_cat = categorical(ContryLabel);    %%将其变成一个categorical类型的数组，为分类数组
ContryLabel_int = double(ContryLabel_cat);
TotalContryNum = size(unique(ContryLabel_int),1);   %%去重然后统计国家数
[N,M] = size(Data_cell);

TotalYear = 78;
CountrysStocks = zeros(TotalContryNum+1,TotalYear);   %%表示创建一个以国家为列标签、时间为行标签的表
for i= 1:N
    CountrysStocks(ContryLabel_int(i),Data_cell{i,3}-1944) = Data_cell{i,4};   %%统计每个国家每一年的核武器
end
for i=1:TotalYear   %%统计核武器总量
    CountrysStocks(TotalContryNum+1,i) = sum(CountrysStocks(1:TotalContryNum,i));
end
%% 预测各国核武数量的同时也预测全球核武数量，方便后面使用
data = CountrysStocks(TotalContryNum+1,:)';  %%取最后一列
perVal = 24;
perLayer = 12;
perVal2 = [12,21,24,10,22,18,10,12,10,10];
perLayer2 = [8,10,10,10,10,10,10,10,10,10];
%% 模型训练
if ~exist('training_net2bgloabl.mat','file')  %%就全球核武器进行模型训练
    net = MyTrainNet(data,perVal,perLayer);
    save('training_net2bgloabl.mat','net');
end


for i=1:TotalContryNum    %%每个国家进行训练
    if ~exist(['training_net2b',num2str(i), '.mat' ],'file')
        data0 = CountrysStocks(i,1:78)';%%把每个国家的核武器弄出来
        net2 = MyTrainNet(data0,perVal2(i),perLayer2(i));  %%进行模型训练
        save(['training_net2b',num2str(i), '.mat' ],'net2');%%保存对应的训练模型
    end
end

%% 预测
net = importdata('training_net2bgloabl.mat');
PreYear = 130-perVal;

[p,p2] = MyPerdict(net,data,perVal,PreYear);%%先对总的进行预测，p包括现在和未来，p2则是未来的，两者都表示核武器总量
p_conutry = zeros(TotalContryNum,length(p));    %%代表建立国家*（预测+过去）年份的表
nets = cell(TotalContryNum,1);
for i=1:TotalContryNum
    net2 = importdata(['training_net2b',num2str(i), '.mat' ]);  %%读入对应的模型
    nets{i} = net2;     %%储存每个国家对应训练的神经网络
    data0 = CountrysStocks(i,:)';    %%读入每个国家的核武器总量
    [pp,pp2] = MyPerdict(net2,data0,perVal,PreYear);
    p_conutry(i,:) = pp2;     %%这代表了每个国家未来的预测值
end
len0 = length(data0);

for j=1:PreYear             %%这里的话，则是求
    tempVal = zeros(TotalContryNum,1);    %%暂时变量，这表示
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
X_p = [1945:1:2022];    %%代表原来的图像
X_p_2 = [1945:1:1945+length(p)-1];    %%代表现在与未来

for i=1:TotalContryNum   
    subplot(2,5,i)
    Y_p = CountrysStocks(i,:);
    plot(X_p,Y_p,'r')   %%这个代表了真实值
    hold on
    pp2 = p_conutry(i,:);     %%这个则代表了预测值
    plot(X_p_2,pp2,'b--');
    axis([min(X_p),max(X_p_2),0,max([max(Y_p),max(pp2)])]);
    xlabel('year');
    ylabel('stockpile');
    contrySTR = find(ContryLabel_int == i);
    legend({'真实值','预测值'});
    title(ContryLabel{contrySTR(1)})
end


%% 函数
function net = MyTrainNet(data,perVal,perLayer)
    force=data;
    T=tonndata(force,false,false);  %输入和输出矩阵须为cell类型的矩阵，且不能用num2cell来转换，如果使用二维cell矩阵，将会被认为是两个输入从而不能训练?
    trainFcn = 'trainbr';   %默认的lmh函数训练时间序列效果很差，采用贝叶斯正则化算泿

    feedbackDelays = 1:perVal;    %延迟向量
    hiddenLayerSize = perLayer;   %%隐藏层数量
    net = narnet(feedbackDelays,hiddenLayerSize,'open',trainFcn);   %%创建非线性自回归神经网络
    [Xs,Xi,Ai,Ts] = preparets(net,{},{},T);       %%数据预处理
    net.divideParam.trainRatio = 70/100;
    net.divideParam.valRatio = 15/100;      %%三个参数的设定
    net.divideParam.testRatio = 15/100;
    net = train(net,Xs,Ts,Xi,Ai);      %%进行训练
    view(net);
end

function [p,p2] = MyPerdict(net,data,perVal,PreYear)%%这个是总的预测
    len = length(data);    
    p = zeros(1,len+perVal);
    p2 = p;      
    p(1:perVal)= data(1:perVal);       %前perVal个不预测直接用现成的，这里的意思是数组的1到24
    for i=1:len-perVal     %依次用perVal个准确的值预测下一个
        ytest = num2cell(data(i:i + perVal)');   %%下一个数据就用前面的已经预测过的时间来预测
        [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);    %%数据初始化
        temp1 = net(AA,AB,AC);     %%创建神经网络
        p(i+perVal) = temp1{1};      
        p2(i+perVal) = round(p(i+perVal)*0.15 + data(i+perVal)*0.85); 
    end
    %p2 = round(p);
    if PreYear>0
        for i=1:PreYear
            %迭代预测后续
            ytest = num2cell(p(len+i-perVal-1:len+i-1));  %%len之后的数据用len之前的数据进行预测
            [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);
            temp1 = net(AA,AB,AC);
            p(i+len) = temp1{1};
            p2(i+len) = ceil(p(i+len));
        end
    end
end

function p3 = MyPerdict2(net,data2,perVal)
    ytest = num2cell(data2);
    [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);    %%进行数据预处理
    temp1 = net(AA,AB,AC);   %%神经网络训练
    p3 = ceil(temp1{1});
end
