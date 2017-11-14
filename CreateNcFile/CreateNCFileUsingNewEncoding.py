import netCDF4 as netcdf_helpers
import MySQLdb
import numpy as np
import datetime

global punchNumber
punchNumber = 0

global sentenceNumberColumn
sentenceNumberColumn = 3


def create_mysql_connection():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="mstdb",  # name of the data base
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')
    global cur
    cur = db.cursor()


def get_all_letters_of_corresponding_dataset_type(type_of_dataset):
    execute_calculate_total_number_Of_sentences_startTime = datetime.datetime.now()

    listOfSelectedLettersAndSentencesQuery = "select UnDiacritizedCharacter, DiacritizedCharacter, LetterType, SentenceNumber," \
                                             " Word, InputSequenceEncodedWords, TargetSequenceEncodedWords " \
                                             "from ParsedDocument where LetterType=" + "'%s'" % type_of_dataset

    cur.execute(listOfSelectedLettersAndSentencesQuery)
    global listOfSelectedLettersAndSentences
    listOfSelectedLettersAndSentences = []
    listOfSelectedLettersAndSentences = cur.fetchall()

    executecalculateTotalNumberOfSentencesEndTime = datetime.datetime.now()
    print "get_all_letters_of_corresponding_dataset_type takes : ", executecalculateTotalNumberOfSentencesEndTime - \
                                                      execute_calculate_total_number_Of_sentences_startTime


def create_netcdf_label():
    execute_create_NetCDF_Label_StartTime = datetime.datetime.now()

    cur.execute("select distinct DiacritizedCharacter,TargetSequenceEncodedWords from parseddocument")
    list_of_labels = np.array(cur.fetchall())
    labels = list_of_labels[:, 1]
    label_list_after_removing_spaces_and_dots = []
    for eachItem in labels:
        selectedLabel = netcdf_helpers.stringtochar(np.array(eachItem))
        test = [str(x) for x in selectedLabel if
                (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
        label_list_after_removing_spaces_and_dots.append(test)

    global purifiedLabels
    purifiedLabels = []
    purifiedLabels = netcdf_helpers.stringtochar(np.array(label_list_after_removing_spaces_and_dots))

    executecreate_netcdf_labelEndTime = datetime.datetime.now()
    print "create_netcdf_label takes : ", executecreate_netcdf_labelEndTime - execute_create_NetCDF_Label_StartTime


def get_selected_letters_in_this_loop(start_range, end_range):
    get_selected_letters_in_this_loopStartTime = datetime.datetime.now()

    global selected_letters_in_this_loop
    selected_letters_in_this_loop = []

    selected_letters_in_this_loop = []
    [selected_letters_in_this_loop.append(item) for item in listOfSelectedLettersAndSentences
     if int(start_range) <= int(item[sentenceNumberColumn]) < int(end_range)]

    get_selected_letters_in_this_loopEndTime = datetime.datetime.now()
    print "get_selected_letters_in_this_loop takes : ", \
        get_selected_letters_in_this_loopEndTime - get_selected_letters_in_this_loopStartTime


def create_netcdf_input():
    executecreate_netcdf_inputStartTime = datetime.datetime.now()

    global purifiedCDFInput
    purifiedCDFInput = []

    listOfExtractedCode = []

    for eachItem in selected_letters_in_this_loop:
        listOfExtractedCode.append(str(eachItem[5]))

    listNetCDFCode = netcdf_helpers.stringtochar(np.array(listOfExtractedCode))
    del listOfExtractedCode[:]

    input_list_after_removing_spaces_and_dots = []
    for eachRow in listNetCDFCode:
        test = [x for x in eachRow if
                (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
        input_list_after_removing_spaces_and_dots.append(test)

    purifiedCDFInput = netcdf_helpers.stringtochar(np.array(input_list_after_removing_spaces_and_dots))
    del input_list_after_removing_spaces_and_dots[:]

    executecreate_netcdf_inputEndTime = datetime.datetime.now()
    print "create_netcdf_input takes : ", executecreate_netcdf_inputEndTime - executecreate_netcdf_inputStartTime


def create_netcdf_seq_length():
    executecreate_netcdf_seq_lengthStartTime = datetime.datetime.now()
    letterCounterForEachSentence = 0
    global SEQLengths
    SEQLengths = []
    sentenceNumber = selected_letters_in_this_loop[0][3]

    # Create Data of SEQ Length Variable
    for eachItem in range(0, len(selected_letters_in_this_loop)):

        if selected_letters_in_this_loop[eachItem][3] == sentenceNumber:
            letterCounterForEachSentence += 1
        else:
            SEQLengths.append(letterCounterForEachSentence)
            sentenceNumber = selected_letters_in_this_loop[eachItem][3]
            letterCounterForEachSentence = 1

    SEQLengths.append(letterCounterForEachSentence)
    executecreate_netcdf_seq_lengthEndTime = datetime.datetime.now()
    print "create_netcdf_seq_length takes : ", executecreate_netcdf_seq_lengthEndTime - executecreate_netcdf_seq_lengthStartTime


def create_netcdf_target_classes():
    executecreate_netcdf_target_classesStartTime = datetime.datetime.now()

    global purifiedTargetClasses
    purifiedTargetClasses = []

    listOfExtractedCode = []

    for eachItem in selected_letters_in_this_loop:
        listOfExtractedCode.append(str(eachItem[6]))

    listNetCDFCode = netcdf_helpers.stringtochar(np.array(listOfExtractedCode))
    del listOfExtractedCode[:]

    targetClasses_list_after_removing_spaces_and_dots = []
    for eachRow in listNetCDFCode:
        test = [x for x in eachRow if
                (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
        targetClasses_list_after_removing_spaces_and_dots.append(test)

    purifiedTargetClasses = netcdf_helpers.stringtochar(
        np.array(targetClasses_list_after_removing_spaces_and_dots).ravel())
    del targetClasses_list_after_removing_spaces_and_dots[:]

    executecreate_netcdf_target_classesEndTime = datetime.datetime.now()
    print "create_netcdf_target_classes takes : ", executecreate_netcdf_target_classesEndTime - \
                                                executecreate_netcdf_target_classesStartTime


#  added due to error in running library
def create_seq_tags():
    executecreate_seq_tagsStartTime = datetime.datetime.now()
    global seqTagSentences
    seqTagSentences = []
    counter = 1
    for eachItem in range(0, len(SEQLengths)):
        sentenceNumber = counter

        # converted to string because if int, the library will give error [Attempt to convert between text & numbers]
        seqTagSentences.append(str(sentenceNumber))
        counter += 1

    seqTagSentences = (np.array(seqTagSentences))

    executecreate_seq_tagsEndTime = datetime.datetime.now()
    print "create_seq_tags takes : ", executecreate_seq_tagsEndTime - executecreate_seq_tagsStartTime


###
def create_netcdf_file(dataset_type):
    global punchNumber
    punchNumber += 1
    print "punch Number: ", punchNumber
    outputFilename = dataset_type + "NCFile_" + str(punchNumber) + ".nc"

    # create a new .nc file
    dataset = netcdf_helpers.Dataset(outputFilename, 'w', format='NETCDF4')

    # create the dimensions

    dataset.createDimension('numTimesteps', len(purifiedCDFInput))
    dataset.createDimension('inputPattSize', len(purifiedCDFInput[0]))
    dataset.createDimension('numLabels', len(purifiedLabels))
    dataset.createDimension('maxLabelLength', len(purifiedLabels[0]))  # you get this value from the array 'labels'
    dataset.createDimension('numSeqs', len(SEQLengths))
    dataset.createDimension('numTimeSteps', len(purifiedTargetClasses))
    #    dataset.createDimension('width', len(purifiedTargetClasses[0]))

    #  added due to error in running library
    dataset.createDimension('maxSeqTagLength', 1)

    # create the variables

    netCDFLabels = dataset.createVariable('labels', 'S1', ('numLabels', 'maxLabelLength'))
    netCDFLabels[:] = purifiedLabels

    netCDFInput = dataset.createVariable('inputs', 'i4', ('numTimesteps', 'inputPattSize'))
    netCDFInput[:] = purifiedCDFInput

    netCDFSEQLengths = dataset.createVariable('seqLengths', 'i4', 'numSeqs')
    netCDFSEQLengths[:] = SEQLengths

    netCDFTargetClasses = dataset.createVariable('targetClasses', 'i4', 'numTimeSteps')
    netCDFTargetClasses[:] = purifiedTargetClasses

    netCDFSeqTags = dataset.createVariable('seqTags', 'S1', ('numSeqs', 'maxSeqTagLength'))
    netCDFSeqTags[:] = seqTagSentences

    # write the data to disk
    print "writing data to", outputFilename
    dataset.close()


def updateNetCDF():
    dataset = netcdf_helpers.Dataset('validation.nc', 'r+')
    x = dataset.variables['inputs'][:]
    global purifiedCDFInput
    concatenatedArray = np.concatenate(x, purifiedCDFInput)
    # purifiedCDFInput += x
    dataset.variables['inputs'][:] = concatenatedArray
    dataset.close()


if __name__ == "__main__":
    patchSize = 2000

    columnNumberOf_SentenceNumber = 3
    availableDataSetTypes = ['training']
    create_mysql_connection()
    get_all_letters_of_corresponding_dataset_type(availableDataSetTypes[0])
    numberOfLoops = len(listOfSelectedLettersAndSentences)
    create_netcdf_label()
    firstSentenceInThisDSType = int(listOfSelectedLettersAndSentences[0][columnNumberOf_SentenceNumber])

    for punchOfSentences in range(0, numberOfLoops, patchSize):
        startRange = str(punchOfSentences + firstSentenceInThisDSType)
        print "start range:", startRange
        punchOfSentences += patchSize
        endRange = str(punchOfSentences + firstSentenceInThisDSType)
        print "end range:", endRange

        get_selected_letters_in_this_loop(availableDataSetTypes[0], startRange, endRange)
        create_netcdf_input()
        create_netcdf_seq_length()
        create_netcdf_target_classes()
        create_seq_tags()
        create_netcdf_file(availableDataSetTypes[0])

