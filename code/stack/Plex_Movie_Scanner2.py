import Media, VideoFiles
import os.path, difflib
import re

def compareFilenames(elem):
  return elem.parts[0].lower()

def Scan(dir, files, mediaList, subdirs):
  
  # Go through the files and see if any of them need to be stacked.
  stack_dict = {}
  stackDiffs = r'[\da-n]' # These are the characters we are looking for being different across stackable filenames
  stackSuffixes = r'(?:cd|dvd|part|pt|disk|disc|scene)\.?(?:\d+)?$'
  scenePrefixes = r'(?:^scene.\d+|scene.\d+$)'
  
  # Sort the mediaList by filename, so we can do our compares properly
  mediaList[:] = sorted(mediaList, key=compareFilenames)

  # check for monotonically increasing numeric or alphabetic filenames
  count = 0
  monotonicSeries = False
  for mediaItem in mediaList[:-1]:
    # if it didn't start as a monotonic series, it's not going to become one
    if count > 0 and monotonicSeries == False:
      break

    # if items were already stacked by other method, skip this attempt
    if hasattr(mediaItem, 'stacked') and mediaItem.stacked == True:
      continue

    m1 = mediaList[count]
    m2 = mediaList[count + 1]
    f1 = os.path.basename(os.path.splitext(m1.parts[0])[0]).strip().lower()
    f2 = os.path.basename(os.path.splitext(m2.parts[0])[0]).strip().lower()

    initialA = re.search(r'(^\d+)', f1)
    initialB = re.search(r'(^\d+)', f2)
    terminalA = re.search(r'(\d+)$', f1)
    terminalB = re.search(r'(\d+)$', f2)

    # if the filenames both start, or both end with a digit, 
    # and the digit of the second filename is 1 larger than the one of the first filename, it's a series
    if(((initialA and initialB) and (int(initialA.group(0)) == int(initialB.group(0)) - 1)) or
      ((terminalA and terminalB) and (int(terminalA.group(0)) == int(terminalB.group(0)) - 1))):
      monotonicSeries = True

    # if the filenames both start, or both end with a letter, 
    # and the letter seems to the correct one for this iteration if we started from "a", 
    # and the letter of the second filename is 1 larger than the one of the first filename, it's a series
    if(monotonicSeries == False):
      initialA = re.search(r'(^[a-y])', f1)
      initialB = re.search(r'(^[a-y])', f2)
      terminalA = re.search(r'([a-y])$', f1)
      terminalB = re.search(r'([a-y])$', f2)
      if(((initialA and initialB) and (ord(initialA.group(0)) == ord('a') + count and ord(initialA.group(0)) == ord(initialB.group(0)) - 1)) or
        ((terminalA and terminalB) and (ord(terminalA.group(0)) == ord('a') + count and ord(terminalA.group(0)) == ord(terminalB.group(0)) - 1))):
        monotonicSeries = True

    if monotonicSeries:

      m1.name = dir
      root = '_monotonic'

      m1.stacked = True
      if stack_dict.has_key(root):
        stack_dict[root].append(m2)
        # only mark the second item as stacked on last iteration, otherwise it'll break out of the loop in the start
        if count == len(mediaList) - 1:
          m2.stacked = True
      else:
        stack_dict[root] = [m1]
        stack_dict[root].append(m2)

    count += 1

  # group scene-based movie splits into a stack
  for mediaItem in mediaList:
    # if items were already stacked by other method, skip this attempt
    if hasattr(mediaItem, 'stacked') and mediaItem.stacked == True:
      continue

    f1 = os.path.basename(os.path.splitext(mediaItem.parts[0])[0]).lower()
    if re.match(scenePrefixes, f1):
      (name, year) = VideoFiles.CleanName(re.sub(scenePrefixes, '', f1))
      root = '_scene'
      mediaItem.name = name

      if stack_dict.has_key(root):
        stack_dict[root].append(mediaItem)
        mediaItem.stacked = True
      else:
        stack_dict[root] = [mediaItem]
        mediaItem.stacked = True

  # Search for prefix-based part names.
  count = 0
  for mediaItem in mediaList[:-1]:
    m1 = mediaList[count]
    m2 = mediaList[count + 1]
    
    # if items were already stacked by other method, skip this attempt
    if hasattr(m1, 'stacked') and m1.stacked == True:
      continue

    f1 = os.path.basename(m1.parts[0])
    f2 = os.path.basename(m2.parts[0])
    
    opcodes = difflib.SequenceMatcher(None, f1, f2).get_opcodes()

    if len(opcodes) == 3: # We only have one transform
      (tag, i1, i2, j1, j2) = opcodes[1]
      if tag == 'replace': # The transform is a replace
        if (i2-i1 <= 2) and (j2-j1 <= 2): # The transform is only one character
          if re.search(stackDiffs, f1[i1:i2].lower()): # That one character is 1-4 or a-n
            root = f1[:i1].strip(' _-')
            xOfy = False

            if f1[i1+1:].lower().strip().startswith('of'): #check to see if this an x of y style stack, if so flag it
              xOfy = True
            #prefix = f1[:i1] + f1[i2:]
            #(root, ext) = os.path.splitext(prefix)
              
            # This is a special case for folders with multiple Volumes of a series (not a stacked movie) [e.g, Kill Bill Vol 1 / 2]
            if not root.lower().strip().endswith('vol') and not root.lower().strip().endswith('volume'): 
              
              # Strip any suffixes like CD, DVD.
              foundSuffix = False
              suffixMatch = re.search(stackSuffixes, root.lower().strip())

              if suffixMatch:
                root = root[0:-len(suffixMatch.group(0))].strip(' _-')
                foundSuffix = True
              
              if foundSuffix or xOfy:
                # Replace the name, which probably had the suffix.
                (name, year) = VideoFiles.CleanName(root)
                # pdb.set_trace()
                
                mediaItem.name = name
                m1.stacked = True
                if stack_dict.has_key(root):
                  stack_dict[root].append(m2)
                  # only mark the second item as stacked on last iteration, otherwise it'll break out of the loop in the start
                  if count == len(mediaList) - 1:
                    m2.stacked = True
                else:
                  stack_dict[root] = [m1]
                  stack_dict[root].append(m2)
    count += 1

  # combine stacks if possible
  count = 0
  stacks = stack_dict.keys()
  for stack in stacks[:-1]:
    s1 = stacks[count]
    s2 = stacks[count + 1]
    opcodes = difflib.SequenceMatcher(None, s1, s2).get_opcodes()
    
    if len(opcodes) == 2: # We only have one transform
      (tag, i1, i2, j1, j2) = opcodes[1]
      if tag == 'replace': # The transform is a replace
        if (i2-i1 == 1) and (j2-j1 == 1): # The transform is only one character
          if re.search(stackDiffs, s1): # That one character is 1-4 or a-n
            root = s1.lower().strip()
            suffixMatch = re.search(stackSuffixes, root)
            if suffixMatch:
              root = root[0:-len(suffixMatch.group(0))].strip(' -')

              (name, year) = VideoFiles.CleanName(root)
              
              # merge existing two stacks into new root
              for oldstack in [s1, s2]:
                for media in stack_dict[oldstack]:
                  media.name = name

                if stack_dict.has_key(root):
                  for media in stack_dict[oldstack]:
                    stack_dict[root].append(media)
                else:
                  stack_dict[root] = stack_dict[oldstack]
                del stack_dict[oldstack]
              
    count += 1

  # Now combine stacked parts
  for stack in stack_dict.keys():
    for media in stack_dict[stack][1:]:
      stack_dict[stack][0].parts.append(media.parts[0])
      mediaList.remove(media)
