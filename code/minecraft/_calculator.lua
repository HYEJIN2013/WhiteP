import("chat")import("math")import("debug")import("./calculator.js")
command("gamerule sendCommandFeedback false")command("scoreboard objectives add calc dummy")command("scoreboard objectives add calcVal dummy")
curr = score("@e[type=ArmorStand,x=0,y=5,z=-1,r=0]", "calc")currVal = score("@e[type=ArmorStand,x=0,y=5,z=-1,r=0]", "calcVal")
containsBrackets = falsecontainsSpecial = falsecontainsPow = falsecontainsMultiplication = falsecontainsAddition = false
function readInput()    local input = -1    repeat
        applyNames() -- do this at first for output
        input = -1        showCalc(input)
        repeat            --wait        until input > 0
        if input == codeOf("(") or input == codeOf(")") then            containsBrackets = true        elseif input == codeOf("sqrt") or input == codeOf("sin") or input == codeOf("cos") then            containsSpecial = true        elseif input == codeOf("^") then            containsPow = true        elseif input == codeOf("*") or input == codeOf("/") then            containsMultiplication = true        elseif input == codeOf("+") or input == codeOf("-") then            containsAddition = true        end
        if input == codeOf("=") then            --nothing        elseif input == codeOf("DEL") then            killCurrent()            moveRight()        elseif input == codeOf("AC") then            command("kill @e[type=ArmorStand,score_calc_min=1]")        else            moveLeft()            command("summon ArmorStand 0 5 -1 {CustomName:\"calc_input\",NoGravity:true,CustomNameVisible:true}")            curr = input        end
    until input == codeOf("=")end
function resetInput()    while "/testfor @e[type=ArmorStand,x=1,y=5,z=-1,r=0]" do        moveRight()    endend
function parseNums()    while "/testfor @e[type=ArmorStand,x=0,y=5,z=-1,r=0]" do
        if curr > 0 and curr < 11 then
            local val = 0.0            repeat                val = val * 10 + curr % 10                killCurrent()                catchFromRight()            until not (curr > 0 and curr < 11)
            if curr == codeOf(".") then                killCurrent()                catchFromRight()
                local pos = 10                repeat                    val = val + float(curr % 10) / pos                    pos = pos * 10
                    killCurrent()                    catchFromRight()                until not (curr > 0 and curr < 11)            end
            extendToRight()            command("summon ArmorStand 0 5 -1 {CustomName:\"Number\",NoGravity:true,CustomNameVisible:true}")            curr = codeOf("__num")            currVal = floatBase(val)
        elseif curr == codeOf("pi") then            curr = codeOf("__num")            currVal = floatBase(PI)        elseif curr == codeOf("e") then            curr = codeOf("__num")            currVal = floatBase(EULER)        elseif curr == codeOf("rnd") then            curr = codeOf("__num")            currVal = random() * 100        end
        moveLeft()    endend
function parseBrackets()    while "/testfor @e[type=ArmorStand,x=0,y=5,z=-1,r=0]" do        if curr == codeOf("(") then            killCurrent()            local indent = 1            repeat                moveLeft()                if curr == codeOf("(") then                    indent = indent + 1                elseif curr == codeOf(")") then                    indent = indent - 1                end            until indent == 0 or not "/testfor @e[type=ArmorStand,x=0,y=5,z=-1,r=0]"
            killCurrent()            resetInput()            parseCurrent()
            moveLeft()            catchFromRight()            moveRight()            moveRight()            catchFromLeft()        end        moveLeft()    endend
function parseSpecial() -- sin cos sqrt    while "/testfor @e[type=ArmorStand,x=0,y=5,z=-1,r=0]" do        local result = 0.0
        if curr == codeOf("sqrt") then            killCurrent()            catchFromRight()
            result = sqrt(floatFromBase(currVal))            currVal = floatBase(result)        elseif curr == codeOf("sin") then            killCurrent()            catchFromRight()
            result = sin(floatFromBase(currVal))            currVal = floatBase(result)        elseif curr == codeOf("cos") then            killCurrent()            catchFromRight()
            result = cos(floatFromBase(currVal))            currVal = floatBase(result)        end
        moveLeft()    endend
function parsePow()    while "/testfor @e[type=ArmorStand,x=0,y=5,z=-1,r=0]" do        if curr == codeOf("^") then            moveRight()
            local left = floatFromBase(currVal)            killCurrent()            catchFromRight()
            killCurrent()            catchFromRight()
            local right = int(floatFromBase(currVal))
            currVal = pow(left, right) * 100        end
        moveLeft()    endend
function parseMultiplication() -- * /    while "/testfor @e[type=ArmorStand,x=0,y=5,z=-1,r=0]" do        if curr == codeOf("*") or curr == codeOf("/") then            moveRight()
            local left = floatFromBase(currVal)            killCurrent()            catchFromRight()
            local op = int(curr)            killCurrent()            catchFromRight()
            local right = floatFromBase(currVal)
            if op == codeOf("*") then                currVal = floatBase(left * right)            elseif op == codeOf("/") then                currVal = floatBase(left / right)            end        end
        moveLeft()    endend
function parseAddition() -- + -    while "/testfor @e[type=ArmorStand,x=0,y=5,z=-1,r=0]" do        if curr == codeOf("+") or curr == codeOf("-") then            moveRight()
            local left = floatFromBase(currVal)            killCurrent()            catchFromRight()
            local op = int(curr)            killCurrent()            catchFromRight()
            local right = floatFromBase(currVal)
            if op == codeOf("+") then                currVal = floatBase(left + right)            elseif op == codeOf("-") then                currVal = floatBase(left - right)            end        end
        moveLeft()    endend


function parseCurrent()    if containsBrackets then        parseBrackets()        resetInput()    end
    if containsSpecial then        parseSpecial()        resetInput()    end
    if containsPow then        parsePow()        resetInput()    end
    if containsMultiplication then        parseMultiplication()        resetInput()    end
    if containsAddition then        parseAddition()        resetInput()    endend

while true do    containsBrackets = false    containsSpecial = false    containsPow = false    containsMultiplication = false    containsAddition = false
    readInput()    resetInput()
    parseNums()    resetInput()
    parseCurrent()
    local result = floatFromBase(currVal)    local negative = false
    if result < 0 then        negative = true        result = result * -1    end
    local left = int(result)    local right = floatBase(result) - left * 100    command("kill @e[type=ArmorStand,score_calc_min=1]")
    if right ~= 0 then
        local digit = right % 10        right = right / 10
        if digit ~= 0 then            moveRight()            command("summon ArmorStand 0 5 -1 {CustomName:\"calc_output\",NoGravity:true,CustomNameVisible:true}")            curr = digit        end
        digit = right % 10        if digit == 0 then            digit = codeOf("0")        end        moveRight()        command("summon ArmorStand 0 5 -1 {CustomName:\"calc_output\",NoGravity:true,CustomNameVisible:true}")        curr = digit
        if false then --wait one tick so current snapshot doesnt fck off armorstand positions for the client        end
        moveRight()        command("summon ArmorStand 0 5 -1 {CustomName:\"calc_output\",NoGravity:true,CustomNameVisible:true}")        curr = codeOf(".")    end
    if left > 0 then        repeat            local digit = left % 10            left = left / 10
            if digit == 0 then                digit = codeOf("0")            end
            moveRight()            command("summon ArmorStand 0 5 -1 {CustomName:\"calc_output\",NoGravity:true,CustomNameVisible:true}")            curr = digit        until left == 0    else        moveRight()        command("summon ArmorStand 0 5 -1 {CustomName:\"calc_output\",NoGravity:true,CustomNameVisible:true}")        curr = codeOf("0")    end
    if negative then        moveRight()        command("summon ArmorStand 0 5 -1 {CustomName:\"calc_output\",NoGravity:true,CustomNameVisible:true}")        curr = codeOf("-")
        if false then --wait one tick so current snapshot doesnt fck off armorstand positions for the client        end
        moveRight()        command("summon ArmorStand 0 5 -1 {CustomName:\"calc_output\",NoGravity:true,CustomNameVisible:true}")        curr = codeOf("0")    end
    while "/testfor @e[type=ArmorStand,x=-1,y=5,z=-1,r=0]" do        moveLeft()    endend
