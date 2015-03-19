require "boid"

function initializeBoids(numBoids)
  for i=1,numBoids do
    yRand = love.math.random(1, config.window.height)
    xRand = love.math.random(1, config.window.width)
    xSpeedRand = math.random() + math.random(0, 3) + 0.25

    if (love.math.random(-1, 2) > 0) then
      xSpeedRand = xSpeedRand * -1
    end
    ySpeedRand = math.random() + math.random(0, 3) + 0.25

    if (love.math.random(-1, 2) > 0) then
      ySpeedRand = ySpeedRand * -1
    end

    boids[i] = Boid:new(nil, i, xRand, yRand, {xSpeedRand, ySpeedRand})
  end
end

function love.load()
  bigFont = love.graphics.newFont(25)
  smallFont = love.graphics.newFont(15)
  started = false
  boids = {}
  numBoids = 80
  showVision = false
  showCollision = false
  initializeBoids(numBoids)
end

function love.keypressed(key)
  if key == "escape" then
    love.event.quit()
  elseif key == " " then
    started = true
  end

  if key == "c" then
    showCollision = not showCollision
  end
  if key == "v" then
    showVision = not showVision
  end
end


function love.update(dt)
  if (started) then
      love.timer.sleep(0.0001)
      for i=1,numBoids do
        boids[i]:applyVelocity()
      end
  end
end

function love.draw()
  -- love.graphics.setBackgroundColor(39, 40, 34)
  if (started) then
    for i=1,numBoids do
      love.graphics.setColor(boids[i].colour)
      love.graphics.polygon("fill", boids[i]:getVertices())
      if showVision then
        love.graphics.circle("line", boids[i].position.x, boids[i].position.y, boids[i].visionRange, 20)
      end
      if showCollision then
        love.graphics.circle("line", boids[i].position.x, boids[i].position.y, boids[i].collisionRange, 20)
      end
    end
  else
    love.graphics.setColor(0, 255, 102)
    love.graphics.setFont(bigFont)
    love.graphics.print("Boids Prototype", config.window.width/2 - 80, config.window.height/2 - 25)
    love.graphics.setFont(smallFont)
    love.graphics.print("Space to start", config.window.width/2 - 30, config.window.width/2)
  end
end
