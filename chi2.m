function chiSquareValue = chi2(encryptedImage)
% 将加密后的图像转为一维数组
encryptedData = encryptedImage(:);

% 计算加密后的图像数据的直方图
histogramData = hist(encryptedData, 0:255);

% 期望的理论分布（可以根据需要进行调整）
expectedDistribution = numel(encryptedData) / numel(histogramData) * ones(size(histogramData));

% 计算卡方值
chiSquareValue = sum((histogramData - expectedDistribution).^2 ./ expectedDistribution);


end


