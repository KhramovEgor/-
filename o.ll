; ModuleID = "my_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %".2" = bitcast [4 x i8]* @"int_fmt_str" to i8*
  %".3" = bitcast [6 x i8]* @"float_fmt_str" to i8*
  %"d" = alloca i32
  store i32 5, i32* %"d"
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %"loop_condition"
loop_condition:
  %".7" = load i32, i32* %"i"
  %".8" = icmp slt i32 %".7", 10
  br i1 %".8", label %"loop_body", label %"after_loop"
loop_body:
  %".10" = load i32, i32* %"d"
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 %".10")
  br label %"loop_modify"
loop_modify:
  %".13" = load i32, i32* %"i"
  %".14" = add i32 %".13", 1
  store i32 %".14", i32* %"i"
  br label %"loop_condition"
after_loop:
  ret i32 0
}

@"int_fmt_str" = global [4 x i8] c"%d\0a\00"
@"float_fmt_str" = global [6 x i8] c"%.6f\0a\00"
declare i32 @"printf"(i8* %".1", ...)
