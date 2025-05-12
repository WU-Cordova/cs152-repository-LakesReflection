### Chosen structures \\
For the menu, I think there are two vaild options. HashMap or Array. The fact that menu items may be accsed in a random order disqaulifes queses and stacks, and anything linked list based, as they are slow to traverse and we expect to traverse alot. Thus we need something indexable, as I primarly expect customers to order via the numbers, as typing out full names is a night mare, the array makes the most sense as its the closet to the index we have been natrruall provided.

Endday-report\\
The end of day report obvs should be a bag, as that is directly the job it was desgined to do. Again Hashmap could also work here, as the bag is mostly just a weird dictonary which is functionally a hashmap. But if we made it we might as well use it and this is basically the ideal use case of bag.\\
\\

Open Orders Que\\
Points 3-4 should operate on the same data structure, as they both are handling the same underlying data (orders).
Since thats true I kinda just need to to defer to the description of item 4, which literalyl calls for a queqe.
The more proper justfication for this is we genrally want to operate on a first come first serve basis as that is least likely to upset customs as it feels fair. First come fist serve is literally just First in First out i.e quese\\
\\

Orders \\
So while Customer Order and Order confirmation are listed as two diffrent structures, I can't figure out why they would be diffrent? Like what diffrent data would in store in the record of the order and record of the order as prestned to customers. Instead I split my orders into Customers- who order some number of isntatined drinks from the menu. The drinks are seperate items.

Total and price are both tracked cause finding total for a bag would be annoying and easier to do as add items
