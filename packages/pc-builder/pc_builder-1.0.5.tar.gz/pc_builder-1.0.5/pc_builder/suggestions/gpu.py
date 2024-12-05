def suggestCompatibleGPUs(userBuild, gpuComp):
    from pc_builder.components.gpu import loadGPUsfromJSON

    suggestedGPUs = []
    allGPUs = loadGPUsfromJSON()

    for gpu in allGPUs:
        isCompatible, compatibility = gpu.checkCompatibility(userBuild)

        if len(suggestedGPUs) == 6:
            break
        if isCompatible:
            suggestedGPUs.append(gpu)

    return suggestedGPUs[:5]
