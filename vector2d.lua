Vector2D = {
	x = 0,
	y = 0,
}

function Vector2D:new(x, y)
	local obj = obj or {}
	obj.__index = self
	obj.x = x
	obj.y = y
	obj.angle = 0
	setmetatable(obj, self)
	self.__index = self
	return obj
end

function Vector2D:getMagnitude()
	return math.sqrt(self.x*self.x + self.y*self.y)
end

function Vector2D:distanceTo(vector)
	return math.sqrt(math.pow(self.x - vector.x, 2) + math.pow(self.y - vector.y, 2))
end

function Vector2D:add(vector, apply)
	local x = self.x + vector.x
	local y = self.y + vector.y
	if (apply ~= nil and apply ~= false) then
		self:setValues(x, y)
		return self
	else
		return Vector2D:new(x, y)
	end
end

function Vector2D:subtract(vector, apply)
	local x = self.x - vector.x
	local y = self.y - vector.y
	if (apply ~= nil and apply ~= false) then
		self:setValues(x, y)
		return self
	else
		return Vector2D:new(x, y)
	end
end

function Vector2D:multiply(multiplier, apply)
	local x = self.x * multiplier
	local y = self.y * multiplier
	if (apply ~= nil and apply ~= false) then
		self:setValues(x, y)
		return self
	else
		return Vector2D:new(x, y)
	end
end

function Vector2D:divide(divisor, apply)
	local x = self.x / divisor
	local y = self.y / divisor
	if (apply ~= nil and apply ~= false) then
		self:setValues(x, y)
		return self
	else
		return Vector2D:new(x, y)
	end
end

function Vector2D:setValues(x, y)
	self.x = x
	self.y = y
end

function Vector2D:normalize(multiplier)
	if (multiplier == nil) then
		multiplier = 1
	end
	if (self.x ~= 0 or self.y ~= 0) then
		local abs = 1 / math.sqrt(self.x*self.x + self.y*self.y)
		self.x = self.x * abs * multiplier
		self.y = self.y * abs * multiplier
	end
end

function Vector2D:rotate(x, y, radAngle, velocity)
	local vy = velocity.y
	local vx = velocity.x
	if (vy > 0) then
		if (vx > 0) then
			radAngle = radAngle - math.pi / 2
		else
		    radAngle = radAngle + math.pi / 2
		end
	else -- y < 0
		if (vx > 0) then
			radAngle = radAngle - math.pi / 2
		else
		    radAngle = radAngle + math.pi / 2
		end
	end

	self.x = self.x - x
	self.y = self.y - y
		
	newX = self.x * math.cos(radAngle) - self.y * math.sin(radAngle); 
	newY = self.x * math.sin(radAngle) + self.y * math.cos(radAngle);
	
	self.x = newX + x
	self.y = newY + y
end

function Vector2D:print(string)
	if (string ~= nil) then
		print(string)
	end
	print('X: ', self.x, '\tY: ', self.y)
end