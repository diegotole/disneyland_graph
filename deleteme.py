class Solution:
    def detectCycle(self, head):

        visited = {}
        idx = 0

        while head is not None:

            if head.val in visited:
                return visited[head.val]

            visited[head.val] = idx
            head = head.next
            idx += 1

        return -1



s = Solution()

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

mylist = [ListNode(3),ListNode(2),ListNode(0),ListNode(-4)]

for idx in range(1, len(mylist)):

    mylist[idx-1].next = mylist[idx]


mylist[3].next = mylist[1]

z= s.detectCycle( mylist[0] )

print(z)
