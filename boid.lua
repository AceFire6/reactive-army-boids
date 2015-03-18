Boid = {
	uid = 0,
	x = 0,
	y = 0,
	rotation = 0,
	velocity = {0, 0},
	maxVelocity = {1.2, 1.2},

	colour = {0, 0, 0},
	massRange = 70,
	collisionRange = 20
}


function Boid:new(obj, uid, x, y, rotation, velocity)
	local obj = obj or {}
	obj.__index = self
	obj.x = x
	obj.y = y
	obj.rotation = rotation * (math.pi / 180)
	obj.velocity = velocity
	obj.colour = {love.math.random(1,255), love.math.random(1,255), love.math.random(1,255)}
	obj.uid = uid
	setmetatable(obj, self)
	self.__index = self
	return obj
end

function Boid:applyVelocity()
	local newVx, newVy = self:centerOfMass()

	self:addVelocity(newVx, newVy)

	print(self.velocity[1], self.velocity[2])

	self.x = self.x + self.velocity[1]
	if (self.x > config.window.width) then
		self.x = 0
	elseif (self.x < 0) then
		self.x = config.window.width
	end

	self.y = self.y + self.velocity[2]
	if (self.y > config.window.height) then
		self.y = 0
	elseif (self.y < 0) then
	    self.y = config.window.height
	end
end

function Boid:addVelocity(x, y)
	self.velocity[1] = self.velocity[1] + x
	self.velocity[2] = self.velocity[2] + y

	if (math.abs(self.velocity[1]) > self.maxVelocity[1]) then
		if (self.velocity[1] < 0) then
			self.velocity[1] = -self.maxVelocity[1]
		else
			self.velocity[1] = self.maxVelocity[1]
		end
	end

	if (math.abs(self.velocity[2]) > self.maxVelocity[2]) then
		if (self.velocity[2] < 0) then
			self.velocity[2] = -self.maxVelocity[2]
		else
			self.velocity[2] = self.maxVelocity[2]
		end
	end
end

function Boid:print()
	print("x: "..self.x, "y: "..self.y, "rotation: "..self.rotation, "velocity: "..self.velocity)
end

function Boid:getVertices()
	return {
		self.x, self.y + 5,
		self.x + 5, self.y - 5,
		self.x - 5, self.y - 5
	}
end

function Boid:printVector(vector)
	print("Printing Vector:")
	for i=1,#vector do
		print(vector[i])
	end
end

function Boid:centerOfMass()
	local xAv = 0
	local yAv = 0
	local neighbours = 0

	for i=1,numBoids do
		if (self.uid ~= boids[i].uid) then
			if (self:distanceTo(self.x, self.y, boids[i].x, boids[i].y) <= self.massRange) then
				xAv = xAv + boids[i].x
				yAv = yAv + boids[i].y
				neighbours = neighbours + 1
			end
		end
	end

	if (neighbours > 0) then
		xAv = xAv / neighbours
		yAv = yAv / neighbours

		xAv = xAv - self.x
		yAv = yAv - self.y

		xAv, yAv = self:normalize(xAv, yAv)
		return xAv/7, yAv/7
	end
	return 0, 0
end

function Boid:normalize(x, y)
	local abs = 1 / math.sqrt(x*x + y*y)
	return abs * x, abs * y
end

function Boid:distanceTo(x1, y1, x2, y2)
	return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
end
