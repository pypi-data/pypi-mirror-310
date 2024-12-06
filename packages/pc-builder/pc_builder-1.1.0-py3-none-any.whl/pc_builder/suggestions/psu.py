def suggestCompatiblePSUs(userBuild, psuComp):
    from pc_builder.components.psu import loadPSUsfromJSON

    suggestedPSUs = []
    allPSUs = loadPSUsfromJSON()

    for psu in allPSUs:
        isCompatible, compatibility = psu.checkCompatibility(userBuild)

        if len(suggestedPSUs) == 6:
            break
        if isCompatible:
            suggestedPSUs.append(psu)

    return suggestedPSUs[:5]
