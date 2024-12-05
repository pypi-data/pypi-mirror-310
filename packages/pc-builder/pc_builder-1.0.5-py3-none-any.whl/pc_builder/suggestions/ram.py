def suggestCompatibleRAMs(userBuild, ramComp):
    from pc_builder.components.ram import loadRAMsfromJSON

    suggestedRAMs = []
    allRAMs = loadRAMsfromJSON()

    for ram in allRAMs:
        isCompatible, compatibility = ram.checkCompatibility(userBuild)

        if len(suggestedRAMs) == 6:
            break
        if isCompatible:
            suggestedRAMs.append(ram)

    return suggestedRAMs[:5]
