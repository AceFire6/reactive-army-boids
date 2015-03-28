require "vector2d"

Boid = {
	uid = 0,
	position = Vector2D:new(0, 0),
	velocity = Vector2D:new(0, 0),

	colour = {0, 0, 0},
	visionRange = 70,
	collisionRange = 25,
	vertices = {Vector2D:new(), Vector2D:new(), Vector2D:new()},
	V_WEIGHT = 0.4,
	CM_WEIGHT = 0.3,
	AV_WEIGHT = 0.6,
	B_WEIGHT = 0.7,
}


function Boid:new(obj, uid, x, y, velocity)
	local obj = obj or {}
	obj.__index = self
	obj.position = Vector2D:new(x, y)
	obj.vertices = {Vector2D:new(x, y + 5), Vector2D:new(x + 5, y - 5), Vector2D:new(x - 5, y - 5)}
	obj.velocity = Vector2D:new(velocity[1], velocity[2])
	obj.colour = {love.math.random(1,255), love.math.random(1,255), love.math.random(1,255)}
	obj.uid = uid
	setmetatable(obj, self)
	self.__index = self
	return obj
end

function Boid:setRanges(collision, vision)
	self.visionRange = self.visionRange + vision
	self.collisionRange = self.collisionRange + collision
end


function Boid:applyVelocity()
	local centerMass = self:moveToCenter()
	local velocityMatching = self:matchVelocity()
	local avoidance = self:avoidNeighbours()
	-- local boundary = self:stayInBounds()

	-- centerMass:print("Center Mass")
	-- velocityMatching:print("Velocity Match")
	-- avoidance:print("Avoidance")
	-- boundary:print("Boundaries")

	centerMass:multiply(self.CM_WEIGHT, true)
	velocityMatching:multiply(self.V_WEIGHT, true)
	avoidance:multiply(self.AV_WEIGHT, true)
	-- boundary:multiply(self.B_WEIGHT, true)

	self.velocity.x = self.velocity.x + centerMass.x + velocityMatching.x + avoidance.x -- + boundary.x
	self.velocity.y = self.velocity.y + centerMass.y + velocityMatching.y + avoidance.y -- + boundary.y

	self.velocity:normalize(1)
	-- self.velocity:print("Velocity")

	self.position:add(self.velocity, true)

	if (self.position.x > config.window.width) then
		self.position.x = 1
	elseif (self.position.x < 0) then
		self.position.x = config.window.width
	end
	
	if (self.position.y > config.window.height) then
		self.position.y = 1
	elseif (self.position.y < 0) then
	    self.position.y = config.window.height
	end

	self:generateVertices(self.position.x, self.position.y)
end

function Boid:stayInBounds()
	local acceleration = Vector2D:new()

	if (self.position.x > config.window.width) then
		acceleration.x = -3
	elseif (self.position.x < 0) then
		acceleration.x = 3
	end
	
	if (self.position.y > config.window.height) then
		acceleration.y = -3
	elseif (self.position.y < 0) then
	    acceleration.y = 3
	end
	acceleration:normalize()
	return acceleration
end

function Boid:moveToCenter()
	local neighbours = 0
	local acceleration = Vector2D:new()

	for i=1,#boids do
		if (self.uid ~= boids[i].uid) then
			if (self.position:distanceTo(boids[i].position) < self.visionRange) then
				acceleration:add(boids[i].position, true)
				neighbours = neighbours + 1
			end
		end
	end

	if (neighbours == 0) then
		return acceleration
	end

	acceleration:divide(neighbours)
	acceleration = Vector2D:new(acceleration.x - self.position.x, acceleration.y - self.position.y)
	acceleration:normalize()
	return acceleration
end

function Boid:matchVelocity()
	local neighbours = 0
	local acceleration = Vector2D:new()

	for i=1,#boids do
		if (self.position:distanceTo(boids[i].position) < self.visionRange) then
			acceleration:add(boids[i].velocity, true)
			neighbours = neighbours + 1
		end
	end

	if (neighbours == 0) then
		return acceleration
	end

	acceleration:divide(neighbours)
	acceleration:normalize()
	return acceleration
end

function Boid:avoidNeighbours()
	local neighbours = 0
	local acceleration = Vector2D:new()

	for i=1,#boids do
		if (self.uid ~= boids[i].uid) then
			if (self.position:distanceTo(boids[i].position) < self.collisionRange) then
				acceleration:add(boids[i].position:subtract(self.position), true)
				neighbours = neighbours + 1
			end
		end
	end

	if (neighbours == 0) then
		return acceleration
	end

	acceleration:divide(neighbours, true)
	acceleration:normalize()
	acceleration:multiply(-1, true)
	return acceleration
end

function Boid:generateVertices(x, y)
	self.vertices = {Vector2D:new(x, y + 10), Vector2D:new(x + 5, y - 5), Vector2D:new(x - 5, y - 5)}
	for i=1,#self.vertices do
		self.vertices[i]:rotate(self.position.x, self.position.y, math.atan(self.velocity.y / self.velocity.x), self.velocity)
	end
end

function Boid:getVertices()
	local vertices = {}
	local index = 1
	for i=1,#self.vertices do
		vertices[index] = self.vertices[i].x
		vertices[index + 1] = self.vertices[i].y
		index = index + 2
	end
	return vertices
end
