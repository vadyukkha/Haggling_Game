#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __attribute__((visibility("default")))
#endif

#include <iostream>
#include <vector>
#include <string>

struct Offer {
    int hat = 0;
    int book = 0;
    int ball = 0;
};

Offer create_offer_hat(int cost_hat, int cost_book, int cost_ball)  {
    Offer offer;
    offer.hat = 0;
    offer.book = 2;
    offer.ball = 3;
    return offer;
}

// Оцениваем стоимость оффера
int evaluate_offer(const Offer& offer, int cost_hat, int cost_book, int cost_ball) {
    int total_cost = (offer.hat * cost_hat) + (offer.book * cost_book) + (offer.ball * cost_ball);
    return total_cost;
}

Offer decide_on_offer_hat(const Offer& offer, int cost_hat, int cost_book, int cost_ball) {
    Offer new_offer;
    if (offer.hat > 0) {
        new_offer.ball = 200;
        return new_offer;
    }
    return create_offer_hat(cost_hat, cost_book, cost_ball);
}

// main function for TGbot
extern "C" EXPORT int decide(int turn, int cost_hat, int cost_book, int cost_ball, int count_hat, int count_book, int count_ball) {
    int a = -1e9;
    if (turn == 0) {
        Offer offer = create_offer_hat(cost_hat, cost_book, cost_ball);
        std::string ans = std::to_string(offer.hat) + std::to_string(offer.book) + std::to_string(offer.ball);
        a = std::stoi(ans);
    }
    else if (turn == 1) {
        Offer enemy_offer;
        enemy_offer.hat = count_hat;
        enemy_offer.book = count_book;
        enemy_offer.ball = count_ball;
        Offer answer = decide_on_offer_hat(enemy_offer, cost_hat, cost_book, cost_ball);
        std::string ans = std::to_string(answer.hat) + std::to_string(answer.book) + std::to_string(answer.ball);
        a = std::stoi(ans);
    }
    else if (turn == 2) {
        Offer enemy_offer;
        enemy_offer.hat = count_hat;
        enemy_offer.book = count_book;
        enemy_offer.ball = count_ball;
        Offer answer = decide_on_offer_hat(enemy_offer, cost_hat, cost_book, cost_ball);
        std::string ans = std::to_string(answer.hat) + std::to_string(answer.book) + std::to_string(answer.ball);
        a = std::stoi(ans);
    }
    else if (turn == 3) {
        Offer enemy_offer;
        enemy_offer.hat = count_hat;
        enemy_offer.book = count_book;
        enemy_offer.ball = count_ball;
        Offer answer = decide_on_offer_hat(enemy_offer, cost_hat, cost_book, cost_ball);
        std::string ans = std::to_string(answer.hat) + std::to_string(answer.book) + std::to_string(answer.ball);
        a = std::stoi(ans);
    }
    else if (turn == 4) {
        Offer enemy_offer;
        enemy_offer.hat = count_hat;
        enemy_offer.book = count_book;
        enemy_offer.ball = count_ball;
        Offer answer = decide_on_offer_hat(enemy_offer, cost_hat, cost_book, cost_ball);
        std::string ans = std::to_string(answer.hat) + std::to_string(answer.book) + std::to_string(answer.ball);
        a = std::stoi(ans);
    }
    else if (turn == 5) {
        Offer enemy_offer;
        enemy_offer.hat = count_hat;
        enemy_offer.book = count_book;
        enemy_offer.ball = count_ball;
        Offer answer = decide_on_offer_hat(enemy_offer, cost_hat, cost_book, cost_ball);
        std::string ans = std::to_string(answer.hat) + std::to_string(answer.book) + std::to_string(answer.ball);
        a = std::stoi(ans);
    }
    return a;
}
