# --- 1. 初始化数据 ---
room_map = [
    ["#", "#", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", "?", ".", "#"], # (1, 4) 是日历
    ["#", ".", "#", "#", ".", ".", "D"], # (2, 6) 是门
    ["#", ".", ".", ".", ".", "?", "#"], # (3, 5) 是铁盒
    ["#", "#", "#", "#", "#", "#", "#"]
]

player_pos = [3, 3]

# 物品描述及初始物品
clues_data = {
    (1, 4): {
        "text": "书桌上放着一本日历，上面用红笔圈出了【10月24日】。",
        "item": "日历"
    },
    (3, 5): {
        "text": "一个上了锁的铁盒子，上面有个4位数的密码锁。",
        "item": None
    }
}

inventory = []  # 背包
is_box_open = False  # 铁盒是否已打开

move_offsets = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1)
}

# --- 2. 画面渲染函数 ---
def render_screen(grid, pos, msg, inv):
    print("\n" * 20)
    print("=== 逃离密室：第一章 ===")
    for r in range(len(grid)):
        line = []
        for c in range(len(grid[r])):
            if r == pos[0] and c == pos[1]:
                line.append("@")
            elif (r, c) == (3, 5) and is_box_open:
                # 如果盒子开了，把铁盒变成平地
                line.append(".")
            else:
                line.append(grid[r][c])
        print(" ".join(line))
    print("========================")
    print(f"【背包】: {inv if inv else '空'}")
    print("========================")
    if msg:
        print(f"▶ {msg}")

# --- 3. 游戏主循环 ---
status_msg = "你醒来发现自己身处密室。w/a/s/d 移动，e 调查，q 退出"

while True:
    render_screen(room_map, player_pos, status_msg, inventory)
    cmd = input("请输入指令: ").strip()

    if cmd == "q":
        print("游戏已退出。")
        break

    # ========== 处理数字密码 1024 ==========
    if cmd == "1024":
        r, c = player_pos
        if (r, c) == (3, 5) and not is_box_open:
            status_msg = "密码正确！咔嚓一声，铁盒打开了。你发现里面静静躺着一把【黄铜钥匙】！"
            inventory.append("黄铜钥匙")
            is_box_open = True
        else:
            status_msg = "这里没有可以输入密码的东西。"
    
    # ========== 处理移动逻辑 ==========
    elif cmd in move_offsets:
        dr, dc = move_offsets[cmd]
        next_r = player_pos[0] + dr
        next_c = player_pos[1] + dc
        target_cell = room_map[next_r][next_c]
        
        # 碰到墙壁
        if target_cell == "#":
            status_msg = "砰！你撞到了冰冷的墙壁，此路不通。"
        # 碰到门
        elif target_cell == "D":
            if "黄铜钥匙" in inventory:
                print("\n*** 你拿出黄铜钥匙，轻轻一扭。咔哒，门开了！ ***")
                print("*** 你成功逃出了密室！恭喜通关！ ***\n")
                break
            else:
                status_msg = "门被紧紧锁住了。你需要一把钥匙才能打开它。"
        else:
            player_pos = [next_r, next_c]
            status_msg = "你向前走了一步。"

    # ========== 处理调查逻辑 (e) ==========
    elif cmd == "e":
        r, c = player_pos
        current_pos = (r, c)
        
        if current_pos in clues_data:
            info = clues_data[current_pos]
            
            # 如果铁盒已经打开了
            if (r, c) == (3, 5) and is_box_open:
                status_msg = "铁盒已经打开了，里面空空如也。"
            else:
                status_msg = info["text"]
                # 获取物品
                item = info["item"]
                if item and item not in inventory:
                    inventory.append(item)
                    status_msg += f"\n✅ 你获得了道具：【{item}】"
                    # 拿完日历后，日历在地图上消失
                    if item == "日历":
                        room_map[1][4] = "."
        else:
            status_msg = "这里没有什么值得注意的东西。"

    else:
        status_msg = "无效指令！请使用 w/a/s/d 移动，e 调查，或在铁盒前输入密码。"