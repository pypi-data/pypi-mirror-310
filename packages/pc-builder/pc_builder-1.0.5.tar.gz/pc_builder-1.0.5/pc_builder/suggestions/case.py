def suggestCompatibleCases(userBuild, caseComp):
    from pc_builder.components.case import loadCasesfromJSON

    suggestedCases = []
    allCases = loadCasesfromJSON()

    for case in allCases:
        isCompatible, compatibility = case.checkCompatibility(userBuild)

        if len(suggestedCases) == 6:
            break
        if isCompatible:
            suggestedCases.append(case)

    return suggestedCases[:5]
