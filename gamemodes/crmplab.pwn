#include <a_samp>

#define COLOR_INFO 0xD4C2FFFF
#define COLOR_OK 0x9FE6B5FF
#define COLOR_WARN 0xFFD08AFF
#define COLOR_WHITE 0xFFFFFFFF

#define START_X 1686.3
#define START_Y -2240.8
#define START_Z 13.5

new bool:gWorking[MAX_PLAYERS];
new gStop[MAX_PLAYERS];
new gDeliveries[MAX_PLAYERS];
new gExperience[MAX_PLAYERS];

new const Float:gRoute[][3] = {
    {1698.6, -2231.2, 13.5},
    {1725.9, -2229.0, 13.5},
    {1748.5, -2239.1, 13.5},
    {1721.1, -2254.0, 13.5}
};

stock SetDeliveryPoint(playerid)
{
    new point = gStop[playerid];
    SetPlayerCheckpoint(playerid, gRoute[point][0], gRoute[point][1], gRoute[point][2], 3.0);
}

stock ShowStats(playerid)
{
    new msg[144];
    format(msg, sizeof msg, "Balance: $%d | Level: %d | EXP: %d/100 | Deliveries: %d",
        GetPlayerMoney(playerid), 1 + gExperience[playerid] / 100,
        gExperience[playerid] % 100, gDeliveries[playerid]);
    return SendClientMessage(playerid, COLOR_WHITE, msg);
}

public OnGameModeInit()
{
    SetGameModeText("CRMPLAB prototype");
    ShowPlayerMarkers(1);
    ShowNameTags(1);
    SetWorldTime(12);
    AddPlayerClass(60, START_X, START_Y, START_Z, 90.0, 0, 0, 0, 0, 0, 0);
    AddStaticVehicle(420, 1680.0, -2244.0, 13.3, 90.0, 6, 1);
    AddStaticVehicle(478, 1674.0, -2244.0, 13.3, 90.0, 1, 1);
    Create3DTextLabel("CRMPLAB: DELIVERY DEPOT\nUse /work to start", COLOR_INFO,
        START_X, START_Y, START_Z + 1.0, 30.0, 0, 0);
    print("CRMPLAB prototype started");
    return 1;
}

public OnPlayerConnect(playerid)
{
    gWorking[playerid] = false;
    gStop[playerid] = 0;
    gDeliveries[playerid] = 0;
    gExperience[playerid] = 0;
    SendClientMessage(playerid, COLOR_INFO, "CRMPLAB test server. Type /help for commands.");
    SendClientMessage(playerid, COLOR_WARN, "Prototype: progress is not saved and accounts are not protected.");
    return 1;
}

public OnPlayerSpawn(playerid)
{
    if (gWorking[playerid]) SetDeliveryPoint(playerid);
    return 1;
}

public OnPlayerDeath(playerid, killerid, reason)
{
    if (gWorking[playerid])
    {
        gWorking[playerid] = false;
        DisablePlayerCheckpoint(playerid);
        SendClientMessage(playerid, COLOR_WARN, "Delivery cancelled. Use /work at the depot to restart.");
    }
    return 1;
}

public OnPlayerCommandText(playerid, cmdtext[])
{
    if (!strcmp(cmdtext, "/help", true))
    {
        SendClientMessage(playerid, COLOR_INFO, "/work - start delivery at the depot | /stopwork - cancel");
        SendClientMessage(playerid, COLOR_INFO, "/stats - balance and progress | /depot - mark depot");
        return 1;
    }
    if (!strcmp(cmdtext, "/stats", true)) return ShowStats(playerid);
    if (!strcmp(cmdtext, "/depot", true))
    {
        if (gWorking[playerid]) return SendClientMessage(playerid, COLOR_WARN, "Cancel the current delivery first with /stopwork.");
        SetPlayerCheckpoint(playerid, START_X, START_Y, START_Z, 4.0);
        return SendClientMessage(playerid, COLOR_INFO, "Depot marked on the map. Use /work when you arrive.");
    }
    if (!strcmp(cmdtext, "/stopwork", true))
    {
        if (!gWorking[playerid]) return SendClientMessage(playerid, COLOR_WARN, "You are not on a delivery.");
        gWorking[playerid] = false;
        DisablePlayerCheckpoint(playerid);
        return SendClientMessage(playerid, COLOR_INFO, "Delivery cancelled.");
    }
    if (!strcmp(cmdtext, "/work", true))
    {
        if (gWorking[playerid]) return SendClientMessage(playerid, COLOR_WARN, "Delivery is already active.");
        if (!IsPlayerInRangeOfPoint(playerid, 12.0, START_X, START_Y, START_Z))
            return SendClientMessage(playerid, COLOR_WARN, "Go to the depot first. Use /depot to find it.");
        gWorking[playerid] = true;
        gStop[playerid] = 0;
        SetDeliveryPoint(playerid);
        return SendClientMessage(playerid, COLOR_OK, "Delivery started: visit the four marked points.");
    }
    return 0;
}

public OnPlayerEnterCheckpoint(playerid)
{
    if (!gWorking[playerid])
    {
        DisablePlayerCheckpoint(playerid);
        SendClientMessage(playerid, COLOR_INFO, "Depot reached. Use /work to begin.");
        return 1;
    }
    gStop[playerid]++;
    if (gStop[playerid] < sizeof gRoute)
    {
        SetDeliveryPoint(playerid);
        SendClientMessage(playerid, COLOR_INFO, "Parcel delivered. Continue to the next point.");
        return 1;
    }
    DisablePlayerCheckpoint(playerid);
    gWorking[playerid] = false;
    gDeliveries[playerid]++;
    gExperience[playerid] += 25;
    GivePlayerMoney(playerid, 250);
    SendClientMessage(playerid, COLOR_OK, "Route complete! +$250 and +25 EXP. Return to the depot for another run.");
    ShowStats(playerid);
    return 1;
}
