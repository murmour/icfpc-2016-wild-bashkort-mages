
let num_0 =
  Num.num_of_int 0

let num_1 =
  Num.num_of_int 1

let num_2 =
  Num.num_of_int 2

let num_neg1 =
  Num.num_of_int (-1)

let num_neg2 =
  Num.num_of_int (-2)

let num_1_by_2 =
  Num.num_of_string "1/2"

let collect action =
  let list = ref [] in
  action (fun item -> list := item :: !list);
  List.rev !list

let items_equal list =
  match list with
    | [] ->
        true
    | x :: xs ->
        List.for_all ((=) x) xs
