def Slice (dictValues, startIndex : int = 0, endIndex : int = -1, step : int = 1) -> list:
	if endIndex == -1:
		endIndex = len(dictValues)
	output = []
	i = 0
	for value in dictValues:
		if i >= endIndex:
			break
		if (i - startIndex) % step == 0:
			output.append(value)
		i += 1
	return output