Boid = {
	x = 0,
	y = 0,
	rotation = 0,
	speed = 0,
}


function Boid:new(obj, x, y, rotation, speed)
	local obj = obj or {}
	obj.__index = self
	obj.x = x
	obj.y = y
	obj.rotation = rotation * (math.pi / 180)
	obj.speed = speed
	setmetatable(obj, self)
	self.__index = self
	return obj
end

function Boid:setRotation(newRotation)
	radianRotation = newRotation * (math.pi / 180)
	self.rotation = radianRotation
end

function Boid:applySpeed()
	-- resolve into x and y components
	xComp = self.speed * math.sin(self.rotation)
	if (self.rotation > 0 and self.rotation < math.pi) then
		xComp = -1 * xComp
	end
	yComp = self.speed * math.cos(self.rotation)
	if (self.rotation > math.pi and self.rotation < (2 * math.pi)) then
		yComp = -1 * yComp
	end

	self.x = self.x + xComp
	if (self.x > config.window.width) then
		self.x = 0
	elseif (self.x < 0) then
	    self.x = config.window.width
	end
	self.y = self.y + yComp
	if (self.y > config.window.height) then
		self.y = 0
	elseif (self.y < 0) then
	    self.y = config.window.height
	end
end

function Boid:print()
	print("x: "..self.x, "y: "..self.y, "rotation: "..self.rotation, "speed: "..self.speed)
end


function Boid:getVertices()
	return {
        self.x, self.y + 5,
        self.x + 5, self.y - 5,
        self.x - 5, self.y - 5
      }
end
