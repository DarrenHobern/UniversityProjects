Darren Hobern 2018

Refresher on my haskell knowledge from uni

\begin{code}
    import qualified Data.Set as Set
    import Data.List
    import Control.Monad
    import Control.Monad.State
\end{code}


\begin{code}

    wordCount :: String -> String
    wordCount [] = []

    lineCount :: String -> Int
    lineCount txt = length $ lines txt

    uniqueWords :: String -> Int
    uniqueWords txt = length $ nub $ words txt
    -- uniqueWords txt = Set.size . Set.fromList $ words txt -- alternative using sets

    longestLine :: String -> Int
    longestLine txt = maximum . map length $ lines txt

    chainedWords :: String -> Int
    chainedWords txt = foldl(\acc x -> if uncurry (==) x then acc+1 else acc) 0 (zip xs (tail xs))
        where
            xs = words txt

\end{code}

Monads monads monads
\begin{code}
-- Implementation of head function using Maybe monad. Returns Nothing if empty list
    maybeHead :: [a] -> Maybe a
    maybeHead [] = Nothing
    maybeHead (x:_) = Just x
-- And last
    maybeLast :: [a] -> Maybe a
    maybeLast [] = Nothing
    maybeLast [x] = Just x
    maybeLast (_:xs) = maybeLast xs

-- It's a box! - it's always a box
    data Box a = Box a deriving (Show, Eq)

    instance Functor Box where
        fmap f (Box a) = Box (f a)

    instance Applicative Box where
        pure = Box
        (<*>) (Box x) = fmap x

    instance Monad Box where
        return = pure
        (Box a) >>= f = f a

-- Stack tack ack ck k
    pop :: State [Int] Int
    pop = state go
        where
            go [] = error "Cannot pop empty stack"
            go (x:xs) = (x,xs)

    push :: Int -> State [Int] ()
    push x = state (\xs -> ((), x:xs))

    dup :: State [Int] ()
    dup = state go
        where
            go [] = error "Cannot duplicate empty stack"
            go xss@(x:_) = ((), x:xss)

    swap :: State [Int] ()
    swap = state go
        where
            go [] = error "Cannot swap empty stack"
            go (x:y:xs) = ((), y:x:xs)
            go xs = ((), xs)


    -- Some stack tests
    stackT1 = flip runState [] $ do
        push 1 -- [1]
        push 2 -- [2,1]
        push 3 -- [3,2,1]
        pop
    -- (3, [2,1])
    stackT2 = flip runState [] $ do
        push 1 -- [1]
        dup    -- [1,1]
        push 3 -- [3,1,1]
        swap   -- [1,3,1]
        x <- pop -- ((1), [3,1])
        push 9 -- [9,3,1]
        push 2 -- [2,9,3,1]
        swap   -- [9,2,3,1]
        push x
    -- ((),[1,9,2,3,1])
    stackT3 = flip runState [1,2,3] $ do
        push 3 -- [3,1,2,3]
        push 5 -- [5,3,1,2,3]
        push 8 -- [8,5,3,1,2,3]
        swap   -- [5,8,3,1,2,3]
        pop    -- ((5),[8,3,1,2,3])
        dup
    -- ((),[8,8,3,1,2,3])
    stackT4 = flip runState (snd stackT2) $ do
        swap -- [9,1,2,3,1]
        pop  -- [1,2,3,1]
        swap -- [2,1,3,1]
        dup
\end{code}
