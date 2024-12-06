def suggestCompatibleCPUcoolers(userBuild, cpucoolerComp):
    from pc_builder.components.cpucooler import loadCPUCoolersfromJSON

    suggestedCoolers = []
    allCoolers = loadCPUCoolersfromJSON()

    for cooler in allCoolers:
        isCompatible, compatibility = cooler.checkCompatibility(userBuild)

        if len(suggestedCoolers) == 6:
            break
        if isCompatible:
            suggestedCoolers.append(cooler)

    return suggestedCoolers[:5]
