require "boid"

function initializeBoids(numBoids)
  for i=1,numBoids do
    yRand = love.math.random(1, config.window.height)
    xRand = love.math.random(1, config.window.width)
    rotRand = love.math.random(0, 360)
    speedRand = love.math.random()

    newBoid = Boid:new(nil, xRand, yRand, rotRand, speedRand)
    table.insert(boidHolder, i, newBoid)
  end
  for i=1,numBoids do
    boidHolder[i]:print()
  end
end

function love.load()
  bigFont = love.graphics.newFont(25)
  smallFont = love.graphics.newFont(15)
  started = false
  boidHolder = {}
  numBoids = 10
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
  if (started == false) then
  else
      for i=1,numBoids do
        boidHolder[i]:applySpeed()
      end  
  end
end

function love.draw()
  love.graphics.setBackgroundColor(39, 40, 34)
  if (started == false) then -- main menu
    love.graphics.setColor(0, 255, 102)
    love.graphics.setFont(bigFont)
    love.graphics.print("Boids Prototype", 150, 200)
    love.graphics.setFont(smallFont)
    love.graphics.print("Space to start", 190, 230)
  else -- flocking
    for i=1,numBoids do
      love.graphics.setColor(i*i*10, i*15, i*13)
      love.graphics.polygon("fill", boidHolder[i]:getVertices())
    end
  end
end
