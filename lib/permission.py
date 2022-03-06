# 必須なものではありませんが、使いやすいように静的クラス関数を定義しています



def canGetInfo(permission: dict) -> bool:
	return permission['info']



class page:
	@classmethod
	def canRead(permission: dict) -> bool:
		return permission['page']['read']
	
	@classmethod
	def canEdit(permission: dict) -> bool:
		return permission['page']['edit']
	
	@classmethod
	def canExistCheck(permission: dict) -> bool:
		return permission['page']['exist']
	
	@classmethod
	def canGetList(permission: dict) -> bool:
		return permission['page']['list']
	
	@classmethod
	def canSearch(permission: dict) -> bool:
		return permission['page']['search']
	
	@classmethod
	def canGetTotal(permission: dict) -> bool:
		return permission['page']['total']



class plugin:
	@classmethod
	def canExecute(permission: dict) -> bool:
		return permission['plugin']['execute']
	
	@classmethod
	def canGetList(permission: dict) -> bool:
		return permission['plugin']['list']
	
	@classmethod
	def canExistCheck(permission: dict) -> bool:
		return permission['plugin']['exist']
	
	@classmethod
	def canGetTotal(permission: dict) -> bool:
		return permission['plugin']['total']



class attach:
	@classmethod
	def canGetTotal(permission: dict) -> bool:
		return permission['attach']['total']
	
	# 予約
	@classmethod
	def canRead(permission: dict) -> bool:
		return permission['attach']['read']



class backup:
	@classmethod
	def canRead(permission: dict) -> bool:
		return permission['backup']['read']
	
	@classmethod
	def canGetTotal(permission: dict) -> bool:
		return permission['backup']['total']



class diff:
	@classmethod
	def canRead(permission: dict) -> bool:
		return permission['diff']['read']
	
	@classmethod
	def canGetTotal(permission: dict) -> bool:
		return permission['diff']['total']