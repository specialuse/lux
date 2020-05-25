from lux.vizLib.altair.AltairRenderer import AltairRenderer

class ViewCollection():
	'''
	ViewCollection is a list of View objects. 
	'''
	def __init__(self,collection):
		self.collection=collection

	def __getitem__(self, key):
		return self.collection[key]
	def __setitem__(self, key, value):
		self.collection[key] = value
	def __len__(self):
		return len(self.collection)
	def __repr__(self):
		import pprint
		x_channel = ""
		largest_mark = 0
		for view in self.collection: #finds longest x attribute among all views
			for spec in view.specLst:
				if spec.channel == "x" and len(x_channel) < len(spec.attribute):
					x_channel = spec.attribute
			if len(view.mark) > largest_mark:
				largest_mark = len(view.mark)
		views_repr = []
		largest_x_length = len(x_channel)
		for view in self.collection: #pads the shorter views with spaces before the y attribute
			x_channel = ""
			y_channel = ""
			for spec in view.specLst:
				if spec.channel == "x":
					x_channel = spec.attribute.ljust(largest_x_length)
				elif spec.channel == "y":
					y_channel = spec.attribute
			aligned_mark = view.mark.ljust(largest_mark)
			views_repr.append(f"<View  (x: {x_channel}, y: {y_channel}) mark: {aligned_mark}, score: {view.score} >") 
		return pprint.pformat(views_repr, indent=2, width = 200)
	def map(self,function):
		# generalized way of applying a function to each element
		return map(function, self.collection)
	
	def get(self,fieldName):
		# Get the value of the field for all objects in the collection
		def getField(dObj):
			fieldVal = getattr(dObj,fieldName)
			# Might want to write catch error if key not in field
			return fieldVal
		return self.map(getField)

	def set(self,fieldName,fieldVal):
		return NotImplemented

	def sort(self, removeInvalid=True, descending = True):
		# remove the items that have invalid (-1) score
		if (removeInvalid): self.collection = list(filter(lambda x: x.score!=-1,self.collection))
		# sort in-place by “score” by default if available, otherwise user-specified field to sort by
		self.collection.sort(key=lambda x: x.score, reverse=descending)

	def topK(self,k):
		#sort and truncate list to first K items
		self.sort()
		return ViewCollection(self.collection[:k])
	def bottomK(self,k):
		#sort and truncate list to first K items
		self.sort(descending=False)
		return ViewCollection(self.collection[:k])
	def normalizeScore(self, invertOrder = False):
		maxScore = max(list(self.get("score")))
		for dobj in self.collection:
			dobj.score = dobj.score/maxScore
			if (invertOrder): dobj.score = 1 - dobj.score

	
	
