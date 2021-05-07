// vJoyClient.cpp : Simple feeder application with a FFB demo
//


// Monitor Force Feedback (FFB) vJoy device
#include "stdafx.h"
//#include "Devioctl.h"
#include "public.h"
#include <malloc.h>
#include <string.h>
#include <stdlib.h>
#include "vjoyinterface.h"
#include "Math.h"

#include <iostream>
#include <string>
#include <stdio.h>
#include "WinUser.h"
#include <map>
#include <algorithm>
#include <list>
#pragma comment (lib, "ws2_32.lib")
#pragma comment (lib, "User32.lib")
#define WIN32_LEAN_AND_MEAN
using namespace std;

int virtual_key_codes[] = {
	0x0D,  //ENTER key
	0x01,  //Left mouse button
	0x02,  //Right mouse button
	0x03,  //Control-break processing
	0x04,  //Middle mouse button (three-button mouse)
	0x05,  //X1 mouse button
	0x06,  //X2 mouse button
	0x07,  //Undefined
	0x08,   //BACKSPACE key
	0x09,   //TAB key
	0x10,   //SHIFT key
	0x11,   //CTRL key
	0x12,   //ALT key
	0x1B,   //ESC key  13
	0x2E,   //DEL key  14
	0x25,   //LEFT ARROW key
	0x26,   //UP ARROW key
	0x27,   //RIGHT ARROW key
	0x28,   //DOWN ARROW key
	0x50,    // P key  19
	0xDC    // \ or |
};

std::map<int, int> XboxMapping_Gunjack{
	{ 0,0},   //left stick vertical
	{ 1,1},   //left stick horizontal
	{ 106,2}, //left stick press
	{ 15,3},  //left-right
	{ 16,4},  //up-down
	{ 99,5},  //X  (left
	{ 96,6},  //A (down
	{ 100,7}, //Y  (up
	{ 97,8},  //B (right
	{ 102,9},  //left trigger L1
	{ 103,10},  //right trigger R1
	{ 17,11},  //left trigger L2
	{ 18,12},  //right trigger R2
	{ 14,13},   //right stick vertical
	{ 11,14},   //right stick horizontal
	{ 107,15},   //right sitck press
	{ 108,16},  //MENU (right
	{ 109,17},  //SYSTEM  (left

};


void split(char** arr, char* str, const char* del) {
	char* s = strtok(str, del);

	while (s != NULL) {
		*arr++ = s;
		s = strtok(NULL, del);
	}
}

// Default device ID (Used when ID not specified)
#define DEV_ID		1

// Prototypes
void  CALLBACK FfbFunction(PVOID data);
void  CALLBACK FfbFunction1(PVOID cb, PVOID data);

BOOL PacketType2Str(FFBPType Type, LPTSTR Str);
BOOL EffectType2Str(FFBEType Ctrl, LPTSTR Str);
BOOL DevCtrl2Str(FFB_CTRL Type, LPTSTR Str);
BOOL EffectOpStr(FFBOP Op, LPTSTR Str);
int  Polar2Deg(BYTE Polar);
int  Byte2Percent(BYTE InByte);
int TwosCompByte2Int(BYTE in);


int ffb_direction = 0;
int ffb_strenght = 0;
int serial_result = 0;


JOYSTICK_POSITION_V2 iReport; // The structure that holds the full position data

int
__cdecl
_tmain(int argc, _TCHAR* argv[])
{
	int stat = 0;
	UINT DevID = DEV_ID;
	USHORT X = 0;
	USHORT Y = 0;
	USHORT Z = 0;
	LONG   Btns = 0;
	

	PVOID pPositionMessage;
	UINT	IoCode = LOAD_POSITIONS;
	UINT	IoSize = sizeof(JOYSTICK_POSITION);
	// HID_DEVICE_ATTRIBUTES attrib;
	BYTE id = 1;
	UINT iInterface = 1;

	// Define the effect names
	static FFBEType FfbEffect= (FFBEType)-1;
	LPCTSTR FfbEffectName[] =
	{"NONE", "Constant Force", "Ramp", "Square", "Sine", "Triangle", "Sawtooth Up",\
	"Sawtooth Down", "Spring", "Damper", "Inertia", "Friction", "Custom Force"};

	// Set the target Joystick - get it from the command-line 
	if (argc>1)
		DevID = _tstoi(argv[1]);

	// Get the driver attributes (Vendor ID, Product ID, Version Number)
	if (!vJoyEnabled())
	{
		_tprintf("Function vJoyEnabled Failed - make sure that vJoy is installed and enabled\n");
		int dummy = getchar();
		stat = - 2;
		goto Exit;
	}
	else
	{
		wprintf(L"Vendor: %s\nProduct :%s\nVersion Number:%s\n", static_cast<TCHAR *> (GetvJoyManufacturerString()), static_cast<TCHAR *>(GetvJoyProductString()), static_cast<TCHAR *>(GetvJoySerialNumberString()));
	};

	// Get the status of the vJoy device before trying to acquire it
	VjdStat status = GetVJDStatus(DevID);

	switch (status)
	{
	case VJD_STAT_OWN:
		_tprintf("vJoy device %d is already owned by this feeder\n", DevID);
		break;
	case VJD_STAT_FREE:
		_tprintf("vJoy device %d is free\n", DevID);
		break;
	case VJD_STAT_BUSY:
		_tprintf("vJoy device %d is already owned by another feeder\nCannot continue\n", DevID);
		return -3;
	case VJD_STAT_MISS:
		_tprintf("vJoy device %d is not installed or disabled\nCannot continue\n", DevID);
		return -4;
	default:
		_tprintf("vJoy device %d general error\nCannot continue\n", DevID);
		return -1;
	};

	// Acquire the vJoy device
	if (!AcquireVJD(DevID))
	{
		_tprintf("Failed to acquire vJoy device number %d.\n", DevID);
		int dummy = getchar();
		stat = -1;
		goto Exit;
	}
	else
		_tprintf("Acquired device number %d - OK\n", DevID);
		


	// Start FFB
#if 1
	BOOL Ffbstarted = FfbStart(DevID);
	if (!Ffbstarted)
	{
		_tprintf("Failed to start FFB on vJoy device number %d.\n", DevID);
		int dummy = getchar();
		stat = -3;
		goto Exit;
	}
	else
		_tprintf("Started FFB on vJoy device number %d - OK\n", DevID);

#endif // 1

	// Register Generic callback function
	// At this point you instruct the Receptor which callback function to call with every FFB packet it receives
	// It is the role of the designer to register the right FFB callback function
	FfbRegisterGenCB(FfbFunction1, NULL);

	////////////////////////////////////////////////////////////
	// INITIALIZE WINSOCK
	////////////////////////////////////////////////////////////

	// Structure to store the WinSock version. This is filled in
	// on the call to WSAStartup()
	WSADATA data;

	// To start WinSock, the required version must be passed to
	// WSAStartup(). This server is going to use WinSock version
	// 2 so I create a word that will store 2 and 2 in hex i.e.
	// 0x0202
	WORD version = MAKEWORD(2, 2);

	// Start WinSock
	int wsOk = WSAStartup(version, &data);
	if (wsOk != 0)
	{
		// Not ok! Get out quickly
		cout << "Can't start Winsock! " << wsOk;
		return 0;
	}


	cout << endl;
	cout << "////////////////////////////////////////////////////////////" << endl;
	cout << "//////////////Listen UDP Packet and Send to SteamVR/////////" << endl;
	cout << "////////////////////////////////////////////////////////////" << endl;
	////////////////////////////////////////////////////////////
	// SOCKET CREATION AND BINDING
	////////////////////////////////////////////////////////////

	// Create a socket, notice that it is a user datagram socket (UDP)
	SOCKET in = socket(AF_INET, SOCK_DGRAM, 0);

	// Create a server hint structure for the server
	sockaddr_in serverHint;
	serverHint.sin_addr.S_un.S_addr = ADDR_ANY; // Us any IP address available on the machine
	serverHint.sin_family = AF_INET; // Address format is IPv4
	serverHint.sin_port = htons(8001); // Convert from little to big endian
	cout << "//////////////Listen to Port 8001 to SteamVR////////////////" << endl;
	cout << "////////////////////////////////////////////////////////////" << endl;
	// Try and bind the socket to the IP and port
	if (bind(in, (sockaddr*)&serverHint, sizeof(serverHint)) == SOCKET_ERROR)
	{
		cout << "Can't bind socket! " << WSAGetLastError() << endl;
		return 0;
	}

	////////////////////////////////////////////////////////////
	// MAIN LOOP SETUP AND ENTRY
	////////////////////////////////////////////////////////////

	sockaddr_in client; // Use to hold the client information (port / ip address)
	int clientLength = sizeof(client); // The size of the client information
	char buf[1024];
	buf[0] = 0;
	// Start endless loop
	// The loop injects position data to the vJoy device
	// If it fails it let's the user try again
	//
	// FFB Note:
	// All FFB activity is performed in a separate thread created when registered the callback function   
	while (1)
	{
		ZeroMemory(&client, clientLength); // Clear the client structure
		ZeroMemory(buf, 1024); // Clear the receive buffer

		// Wait for message
		int bytesIn = recvfrom(in, buf, 1024, 0, (sockaddr*)&client, &clientLength);
		if (bytesIn == SOCKET_ERROR)
		{
			cout << "Error receiving from client " << WSAGetLastError() << endl;
			continue;
		}

		// Display message and client info
		char clientIp[256]; // Create enough space to convert the address byte array
		ZeroMemory(clientIp, 256); // to string of characters

		// split buf
		char* str = buf;
		const char* d = ",";
		char* arr[3];
		split(arr, str, d);
		if (str[0] == '\0')
			continue;

		// Display the message / who sent it
		string type = *arr;
		string keycode, keyvalue;
		int value;
		keycode.assign(arr[1]);
		if (keycode.empty()) {
			keycode = "-1";
			//cout << "Keycode is "<< arr[1] << endl;
		}	else {
			value = stoi(keycode);
		}

		if (strcmp("AxisTouch", *arr) == 0) {
			keyvalue.assign(arr[2]);
		}
		else
			keyvalue.assign("404");

		// Convert from byte array to chars
#if 1
		char* pack_addr;
		pack_addr = inet_ntoa(client.sin_addr);
		//cout << "Message recv from " << pack_addr << " ,Action : " << *arr << ", keycode : " << keycode << ", value: " << stof(keyvalue) << endl;
#endif
		map<int, int>::iterator gunjack_mapping_it;
		gunjack_mapping_it = XboxMapping_Gunjack.find(value);
		if (gunjack_mapping_it != XboxMapping_Gunjack.end())
			value = gunjack_mapping_it->second;
		if (type == "KeyDown") {
			
			Btns |= 1UL << value;
			//keybd_event(virtual_key_codes[value], 0x1E, 0, 0);
		}
		else if (type == "KeyUp") {
			Btns &= ~(1UL << value);
			//keybd_event(virtual_key_codes[value], 0x1F, KEYEVENTF_KEYUP, 0);
		}
		else if (type == "AxisTouch") {
			//cout << value << endl;
			switch (value) {
				case 0://Left Vertical
					iReport.wAxisY = stof(keyvalue) * 32767;
					break;
				case 1://Left Horizontal
					iReport.wAxisX = stof(keyvalue) * 32767;
					break;
				case 3://Cross Left-Right
					if (keyvalue == "-1") {
						Btns |= 1UL << 19;
						Btns &= ~(1UL << 20);
					}
					else if (keyvalue == "1") {
						Btns &= ~(1UL << 19);
						Btns |= 1UL << 20;
					}
					break;
				case 4://Cross Up-Down
					if (keyvalue == "-1") {
						Btns |= 1UL << 21;
						Btns &= ~(1UL << 22);
					}else if (keyvalue == "1") {
						Btns &= ~(1UL << 21);
						Btns |= 1UL << 22;
					}
					break;
				case 11://L2
					iReport.wAxisZ = stof(keyvalue) * 32767;
					break;
				case 12://R2
					iReport.wAxisZRot = stof(keyvalue) * 32767;
					break;
				case 13://Right Vertical
					iReport.wAxisYRot = stof(keyvalue) * 32767;
					break;
				case 14://Right Horizontal
					iReport.wAxisXRot = stof(keyvalue) * 32767;
					break;
			}

		}
		// Set destenition vJoy device
		id = (BYTE)DevID;
		iReport.bDevice = id;

		// Set position data of 3 first axes
		//if (Z>35000) Z=0;
		//Z += 200;
		//iReport.wAxisZ = Z;
		//iReport.wAxisX = 32000-Z;
		//iReport.wAxisY = Z/2+7000;

		// Set position data of first 8 buttons
		//Btns = 1<<(Z/4000);
		iReport.lButtons = Btns;

		// Send position data to vJoy device
		pPositionMessage = (PVOID)(&iReport);
		if (!UpdateVJD(DevID, pPositionMessage))
		{
			printf("Feeding vJoy device number %d failed - try to enable device then press enter\n", DevID);
			getchar();
			AcquireVJD(DevID);
		}
		Sleep(2);
	}

Exit:
	RelinquishVJD(DevID);
	return 0;
}


// Generic callback function
void CALLBACK FfbFunction(PVOID data)
{
	FFB_DATA * FfbData = (FFB_DATA *)data;
	int size = FfbData->size;
	_tprintf("\nFFB Size %d\n", size);
	_tprintf("Cmd:%08.8X ", FfbData->cmd);
	_tprintf("ID:%02.2X ", FfbData->data[0]);
	_tprintf("Size:%02.2d ", static_cast<int>(FfbData->size - 8));
	_tprintf(" - ");
	for (UINT i = 0; i < FfbData->size - 8; i++)
		_tprintf(" %02.2X", (UINT)FfbData->data);
	_tprintf("\n");
}

void CALLBACK FfbFunction1(PVOID data, PVOID userdata)
{
	// Packet Header
	_tprintf("\n ============= FFB Packet size Size %d =============\n", static_cast<int>(((FFB_DATA *)data)->size));

	/////// Packet Device ID, and Type Block Index (if exists)
#pragma region Packet Device ID, and Type Block Index
	int DeviceID, BlockIndex;
	FFBPType	Type;
	TCHAR	TypeStr[100];

	if (ERROR_SUCCESS == Ffb_h_DeviceID((FFB_DATA *)data, &DeviceID))
		_tprintf("\n > Device ID: %d", DeviceID);
	if (ERROR_SUCCESS == Ffb_h_Type((FFB_DATA *)data, &Type))
	{
		if (!PacketType2Str(Type, TypeStr))
			_tprintf("\n > Packet Type: %d", Type);
		else
			_tprintf("\n > Packet Type: %s", TypeStr);

	}
	if (ERROR_SUCCESS == Ffb_h_EBI((FFB_DATA *)data, &BlockIndex))
		_tprintf("\n > Effect Block Index: %d", BlockIndex);
#pragma endregion


	/////// Effect Report
#pragma region Effect Report
	FFB_EFF_CONST Effect;
	if (ERROR_SUCCESS == Ffb_h_Eff_Report((FFB_DATA *)data, &Effect))
	{
		if (!EffectType2Str(Effect.EffectType, TypeStr))
			_tprintf("\n >> Effect Report: %02x", Effect.EffectType);
		else
			_tprintf("\n >> Effect Report: %s", TypeStr);

		if (Effect.Polar)
		{
			_tprintf("\n >> Direction: %d deg (%02x)", Polar2Deg(Effect.Direction), Effect.Direction);


		}
		else
		{
			_tprintf("\n >> X Direction: %02x", Effect.DirX);
			_tprintf("\n >> Y Direction: %02x", Effect.DirY);
		};

		if (Effect.Duration == 0xFFFF)
			_tprintf("\n >> Duration: Infinit");
		else
			_tprintf("\n >> Duration: %d MilliSec", static_cast<int>(Effect.Duration));

		if (Effect.TrigerRpt == 0xFFFF)
			_tprintf("\n >> Trigger Repeat: Infinit");
		else
			_tprintf("\n >> Trigger Repeat: %d", static_cast<int>(Effect.TrigerRpt));

		if (Effect.SamplePrd == 0xFFFF)
			_tprintf("\n >> Sample Period: Infinit");
		else
			_tprintf("\n >> Sample Period: %d", static_cast<int>(Effect.SamplePrd));


		_tprintf("\n >> Gain: %d%%", Byte2Percent(Effect.Gain));

	};
#pragma endregion
#pragma region PID Device Control
	FFB_CTRL	Control;
	TCHAR	CtrlStr[100];
	if (ERROR_SUCCESS == Ffb_h_DevCtrl((FFB_DATA *)data, &Control) && DevCtrl2Str(Control, CtrlStr))
		_tprintf("\n >> PID Device Control: %s", CtrlStr);

#pragma endregion
#pragma region Effect Operation
	FFB_EFF_OP	Operation;
	TCHAR	EffOpStr[100];
	if (ERROR_SUCCESS == Ffb_h_EffOp((FFB_DATA *)data, &Operation) && EffectOpStr(Operation.EffectOp, EffOpStr))
	{
		_tprintf("\n >> Effect Operation: %s", EffOpStr);
		if (Operation.LoopCount == 0xFF)
			_tprintf("\n >> Loop until stopped");
		else
			_tprintf("\n >> Loop %d times", static_cast<int>(Operation.LoopCount));

	};
#pragma endregion
#pragma region Global Device Gain
	BYTE Gain;
	if (ERROR_SUCCESS == Ffb_h_DevGain((FFB_DATA *)data, &Gain))
		_tprintf("\n >> Global Device Gain: %d", Byte2Percent(Gain));

#pragma endregion
#pragma region Condition
	FFB_EFF_COND Condition;
	if (ERROR_SUCCESS == Ffb_h_Eff_Cond((FFB_DATA *)data, &Condition))
	{
		if (Condition.isY)
			_tprintf("\n >> Y Axis");
		else
			_tprintf("\n >> X Axis");
		cout << ">> Center Point Offset: " << TwosCompByte2Int(Condition.CenterPointOffset) * 10000 / 127 << endl;
		cout << ">> Positive Coefficient: " << TwosCompByte2Int(Condition.PosCoeff) * 10000 / 127 << endl;
		cout << ">> Negative Coefficient: " << TwosCompByte2Int(Condition.NegCoeff) * 10000 / 127 << endl;
		cout << ">> Positive Saturation: " << Condition.PosSatur * 10000 / 255 << endl;
		cout << ">> Negative Saturation: " << Condition.NegSatur * 10000 / 255 << endl;
		cout << ">> Dead Band: " << Condition.DeadBand * 10000 / 255 << endl;
		//_tprintf("\n >> Center Point Offset: %d", TwosCompByte2Int(Condition.CenterPointOffset)*10000/127);
		//_tprintf("\n >> Positive Coefficient: %d", TwosCompByte2Int(Condition.PosCoeff)*10000/127);
		//_tprintf("\n >> Negative Coefficient: %d", TwosCompByte2Int(Condition.NegCoeff)*10000/127);
		//_tprintf("\n >> Positive Saturation: %d", Condition.PosSatur*10000/255);
		//_tprintf("\n >> Negative Saturation: %d", Condition.NegSatur*10000/255);
		//_tprintf("\n >> Dead Band: %d", Condition.DeadBand*10000/255);
	}
#pragma endregion
#pragma region Envelope
	FFB_EFF_ENVLP Envelope;
	if (ERROR_SUCCESS == Ffb_h_Eff_Envlp((FFB_DATA *)data, &Envelope))
	{
		_tprintf("\n >> Attack Level: %d", Envelope.AttackLevel*10000/255);
		_tprintf("\n >> Fade Level: %d", Envelope.FadeLevel*10000/255);
		_tprintf("\n >> Attack Time: %d", static_cast<int>(Envelope.AttackTime));
		_tprintf("\n >> Fade Time: %d", static_cast<int>(Envelope.FadeTime));
	};

#pragma endregion
#pragma region Periodic
	FFB_EFF_PERIOD EffPrd;
	if (ERROR_SUCCESS == Ffb_h_Eff_Period((FFB_DATA *)data, &EffPrd))
	{
		_tprintf("\n >> Magnitude: %d", EffPrd.Magnitude * 10000 / 255);
		_tprintf("\n >> Offset: %d", TwosCompByte2Int(EffPrd.Offset) * 10000 / 127);
		_tprintf("\n >> Phase: %d", EffPrd.Phase * 3600 / 255);
		_tprintf("\n >> Period: %d", static_cast<int>(EffPrd.Period));
	};
#pragma endregion

#pragma region Effect Type
	FFBEType EffectType;
	if (ERROR_SUCCESS == Ffb_h_EffNew((FFB_DATA *)data, &EffectType))
	{
		if (EffectType2Str(EffectType, TypeStr))
			_tprintf("\n >> Effect Type: %s", TypeStr);
		else
			_tprintf("\n >> Effect Type: Unknown");
	}

#pragma endregion

#pragma region Ramp Effect
	FFB_EFF_RAMP RampEffect;
	if (ERROR_SUCCESS == Ffb_h_Eff_Ramp((FFB_DATA *)data, &RampEffect))
	{
		_tprintf("\n >> Ramp Start: %d", TwosCompByte2Int(RampEffect.Start) * 10000 / 127);
		_tprintf("\n >> Ramp End: %d", TwosCompByte2Int(RampEffect.End) * 10000 / 127);
	};

#pragma endregion

	_tprintf("\n");
	FfbFunction(data);
	_tprintf("\n ====================================================\n");

}


// Convert Packet type to String
BOOL PacketType2Str(FFBPType Type, LPTSTR OutStr)
{
	BOOL stat = TRUE;
	LPTSTR Str="";

	switch (Type)
	{
	case PT_EFFREP:
		Str = "Effect Report";
		break;
	case PT_ENVREP:
		Str = "Envelope Report";
		break;
	case PT_CONDREP:
		Str = "Condition Report";
		break;
	case PT_PRIDREP:
		Str = "Periodic Report";
		break;
	case PT_CONSTREP:
		Str = "Constant Force Report";
		break;
	case PT_RAMPREP:
		Str = "Ramp Force Report";
		break;
	case PT_CSTMREP:
		Str = "Custom Force Data Report";
		break;
	case PT_SMPLREP:
		Str = "Download Force Sample";
		break;
	case PT_EFOPREP:
		Str = "Effect Operation Report";
		break;
	case PT_BLKFRREP:
		Str = "PID Block Free Report";
		break;
	case PT_CTRLREP:
		Str = "PID Device Contro";
		break;
	case PT_GAINREP:
		Str = "Device Gain Report";
		break;
	case PT_SETCREP:
		Str = "Set Custom Force Report";
		break;
	case PT_NEWEFREP:
		Str = "Create New Effect Report";
		break;
	case PT_BLKLDREP:
		Str = "Block Load Report";
		break;
	case PT_POOLREP:
		Str = "PID Pool Report";
		break;
	default:
		stat = FALSE;
		break;
	}

	if (stat)
		_tcscpy_s(OutStr, 100, Str);

	return stat;
}

// Convert Effect type to String
BOOL EffectType2Str(FFBEType Type, LPTSTR OutStr)
{
	BOOL stat = TRUE;
	LPTSTR Str="";

	switch (Type)
	{
	case ET_NONE:
		stat = FALSE;
		break;
	case ET_CONST:
		Str="Constant Force";
		break;
	case ET_RAMP:
		Str="Ramp";
		break;
	case ET_SQR:
		Str="Square";
		break;
	case ET_SINE:
		Str="Sine";
		break;
	case ET_TRNGL:
		Str="Triangle";
		break;
	case ET_STUP:
		Str="Sawtooth Up";
		break;
	case ET_STDN:
		Str="Sawtooth Down";
		break;
	case ET_SPRNG:
		Str="Spring";
		break;
	case ET_DMPR:
		Str="Damper";
		break;
	case ET_INRT:
		Str="Inertia";
		break;
	case ET_FRCTN:
		Str="Friction";
		break;
	case ET_CSTM:
		Str="Custom Force";
		break;
	default:
		stat = FALSE;
		break;
	};

	if (stat)
		_tcscpy_s(OutStr, 100, Str);

	return stat;
}

// Convert PID Device Control to String
BOOL DevCtrl2Str(FFB_CTRL Ctrl, LPTSTR OutStr)
{
	BOOL stat = TRUE;
	LPTSTR Str="";

	switch (Ctrl)
	{
	case CTRL_ENACT:
		Str="Enable Actuators";
		break;
	case CTRL_DISACT:
		Str="Disable Actuators";
		break;
	case CTRL_STOPALL:
		Str="Stop All Effects";
		break;
	case CTRL_DEVRST:
		Str="Device Reset";
		break;
	case CTRL_DEVPAUSE:
		Str="Device Pause";
		break;
	case CTRL_DEVCONT:
		Str="Device Continue";
		break;
	default:
		stat = FALSE;
		break;
	}
	if (stat)
		_tcscpy_s(OutStr, 100, Str);

	return stat;
}

// Convert Effect operation to string
BOOL EffectOpStr(FFBOP Op, LPTSTR OutStr)
{
	BOOL stat = TRUE;
	LPTSTR Str="";

	switch (Op)
	{
	case EFF_START:
		Str="Effect Start";
		break;
	case EFF_SOLO:
		Str="Effect Solo Start";
		break;
	case EFF_STOP:
		Str="Effect Stop";
		break;
	default:
		stat = FALSE;
		break;
	}

	if (stat)
		_tcscpy_s(OutStr, 100, Str);

	return stat;
}

// Polar values (0x00-0xFF) to Degrees (0-360)
int Polar2Deg(BYTE Polar)
{
	return ((UINT)Polar*360)/255;
}

// Convert range 0x00-0xFF to 0%-100%
int Byte2Percent(BYTE InByte)
{
	return ((UINT)InByte*100)/255;
}

// Convert One-Byte 2's complement input to integer
int TwosCompByte2Int(BYTE in)
{
	int tmp;
	BYTE inv = ~in;
	BOOL isNeg = in>>7;
	if (isNeg)
	{
		tmp = (int)(inv);
		tmp = -1*tmp;
		return tmp;
	}
	else
		return (int)in;
}
