
const int NumPins = 4;
int state = 0;
int board[5] = {0,0,0,0,0};

void setup() {
  Serial.begin(9600);
  for (int i = 1; i <= NumPins; i++){
    pinMode(i, INPUT);
  }
  
}

void loop() {
  for (int y = 1; y <= 4; y++){
    if (y != 3){
      state = analogRead(y);
      if (state != 0){
        if (board[y] != 1){
          board[y] = 1;
        }
        else{
          board[y] = 0;
        }
        for (int x = 1; x <= 4; x++){
        Serial.println(board[x]);
      }
      Serial.println("");
      }
  }
  }
}
