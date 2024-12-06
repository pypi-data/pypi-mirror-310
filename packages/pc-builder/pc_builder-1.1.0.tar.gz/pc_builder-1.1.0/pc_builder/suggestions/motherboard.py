def suggestCompatibleMotherboards(userBuild, motherboardComp):
    from pc_builder.components.motherboard import loadMBsfromJSON

    suggestedMotherboards = []
    allMotherboards = loadMBsfromJSON()

    for motherboard in allMotherboards:
        isCompatible, compatibility = motherboard.checkCompatibility(userBuild)

        if len(suggestedMotherboards) == 6:
            break

        if isCompatible:
            suggestedMotherboards.append(motherboard)

    return suggestedMotherboards[:5]
