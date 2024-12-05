def suggestCompatibleSSDs(userBuild, ssdComp):
    from pc_builder.components.ssd import loadSSDsfromJSON

    suggestedSSDs = []
    allSSDs = loadSSDsfromJSON()
    ssdType = (
        "M.2"
        if any(
            "M.2" in interface for interface in userBuild.selectedPart.specs.interface
        )
        else "SATA"
    )

    for ssd in allSSDs:
        checkingType = (
            "M.2"
            if any("M.2" in interface for interface in ssd.specs.interface)
            else "SATA"
        )
        if checkingType == ssdType:
            isCompatible, compatibility = ssd.checkCompatibility(userBuild)

            if len(suggestedSSDs) == 6:
                break
            if isCompatible:
                suggestedSSDs.append(ssd)

    return suggestedSSDs[:5]
