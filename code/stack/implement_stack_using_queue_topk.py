def partition(nums, left, right):
    smallerIdx = left
    for idx in xrange(left+1, right+1):
        if nums[idx] < nums[left]:
            smallerIdx += 1
            nums[idx], nums[smallerIdx] = nums[smallerIdx], nums[idx]
    nums[smallerIdx], nums[left] = nums[left], nums[smallerIdx]
    return smallerIdx


def topk_util(nums, left, right, k):
    idx = partition(nums, left, right)
    rank = idx-left+1
    if rank == k:
        return nums[idx]
    elif rank < k:
        return topk_util(nums, idx+1, right, k-rank)
    else:
        return topk_util(nums, left, idx-1, k)

def topk(nums, k):
    if len(nums) < k:
        return None
    return topk_util(nums, 0, len(nums)-1, k)

nums = [5, 3, 4, 2, 1]
print topk(nums, 3)
