% 生成期望的均匀分布直方图
function expectedHist = generateExpectedHistogram(imageSize)
    numBins = 256; % 假设使用256个bins
    expectedHist = ones(numBins, 1) * (imageSize / numBins);
end