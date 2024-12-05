def suggestCompatibleHDDs(userBuild, hddComp):
    from pc_builder.components.hdd import loadHDDsfromJSON

    suggestedHDDs = []
    allHDDs = loadHDDsfromJSON()

    for hdd in allHDDs:
        isCompatible, compatibility = hdd.checkCompatibility(userBuild)

        if len(suggestedHDDs) == 6:
            break
        if isCompatible:
            suggestedHDDs.append(hdd)

    return suggestedHDDs[:5]
