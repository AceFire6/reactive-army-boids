require "boid"

function initializeBoids(numBoids)
  for i=1,numBoids do
    yRand = love.math.random(1, config.window.height)
    xRand = love.math.random(1, config.window.width)
    rotRand = love.math.random(0, 360)
    xSpeedRand = love.math.random(0.75, 2)
    ySpeedRand = love.math.random(0.75, 2)

    boids[i] = Boid:new(nil, i, xRand, yRand, rotRand, {xSpeedRand, ySpeedRand})
  end
end

function love.load()
  bigFont = love.graphics.newFont(25)
  smallFont = love.graphics.newFont(15)
  started = false
  boids = {}
  numBoids = 5
  initializeBoids(numBoids)
end

function love.keypressed(key)
  if key == "escape" then
    love.event.quit()
  elseif key == " " then
    started = true
  end
end


function love.update(dt)
  if (started) then
      for i=1,numBoids do
        boids[i]:applyVelocity()
      end
  end
end

function love.draw()
  love.graphics.setBackgroundColor(39, 40, 34)
  if (started) then
    for i=1,numBoids do
      love.graphics.setColor(boids[i].colour)
      love.graphics.polygon("fill", boids[i]:getVertices())
      -- love.graphics.circle("line", com[1], com[2], 10, 8)
      -- love.graphics.circle("line", boids[i].x, boids[i].y, boids[i].collisionRange, 8)
    end
  else
    love.graphics.setColor(0, 255, 102)
    love.graphics.setFont(bigFont)
    love.graphics.print("Boids Prototype", config.window.width/2 - 80, config.window.height/2 - 25)
    love.graphics.setFont(smallFont)
    love.graphics.print("Space to start", config.window.width/2 - 30, config.window.width/2)
  end
end
