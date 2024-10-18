#include <iostream>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>
#include <SFML/Audio.hpp>
#include <vector>
#include <utility>
#include <ctime>


using namespace sf;
using namespace std;

int main() {
	RenderWindow window(VideoMode(500, 800), "flappy bird");
	window.setFramerateLimit(60);

	srand(time(NULL));

	bool main = true;
	bool overr = false;
	bool j;

	float gravity = 1;
	float v = 0;
	float jump = 15;
	int keytime = 5;
	float a = -20;
	int score = 0;
	int pipescount = 0;

	Music music;

	if (!music.openFromFile("./assets/audio/audio_wing.ogg")) {
		cout << "error";
	}
	music.setVolume(20);

	Font font;
	if (!font.loadFromFile("./assets/font/ff.ttf")) {
		cout << "error";
	}
	Text title("Flappy Bird", font);
	title.setCharacterSize(80.f);
	title.setPosition(50.f, 110.f);

	Text tap("Tap to start", font);
	tap.setCharacterSize(40.f);
	tap.setFillColor(Color::Red);
	tap.setPosition(140.f, 550.f);

	Text over("Game over", font);
	over.setCharacterSize(80.f);
	over.setPosition(50.f, 110.f);

	Font fon;
	if (!fon.loadFromFile("./assets/font/tt.ttf")) {
		cout << "Error";
	}

	Text s(to_string(0), fon);
	s.setPosition(window.getSize().x / 2 - 50, 20.f);
	s.setFillColor(Color::Black);
	s.setScale(1.2f, 1.2f);


	Texture texture;
	if (!texture.loadFromFile("./assets/pics/background-night.png")) {
		cout << "Error";
	}
	Sprite background(texture);
	background.setScale(2.1f, 1.6f);

	Texture t;
	if (!t.loadFromFile("./assets/pics/base.png")) {
		cout << "Error";
	}

	Sprite base(t);
	base.setScale(2.f, 2.f);
	base.setPosition(0.f, 650.f);

	Texture b;
	if (!b.loadFromFile("./assets/pics/R.png")) {
		cout << "Error";
	}

	Sprite bird(b);
	bird.setScale(0.09f, 0.09f);
	bird.setPosition(window.getSize().x/2-250*0.09, window.getSize().y/2-170*0.09);

	Texture pi;
	if (!pi.loadFromFile("./assets/pics/pipe.png")) {
		cout << "Error";
	}

	Sprite pip(pi);
	pip.setScale(1.5f, 2.f);

	Sprite rpip(pi);
	rpip.setScale(1.5f, 2.f);
	rpip.setRotation(180);

	vector<pair<Sprite, Sprite>> pipes;

	while (window.isOpen()) {
		Event event;
		while (window.pollEvent(event)) {
			if (event.type == Event::Closed) window.close();
		}

		//Update
		keytime++;
		pipescount++;
		j = false;

		if (!overr) {
			if (main && Keyboard::isKeyPressed(Keyboard::Space) && keytime >=5) {
				main = false;
				pipescount = 0;
				keytime = 0;
				v -= jump;
				score = 0;
				s.setString(to_string(score));
			}
			else if (!main) {
				if (Keyboard::isKeyPressed(Keyboard::Space)) {
					if (keytime >= 10) {
						keytime = 0;
						v = -jump;
						j = true;
						music.play();
					}
				}
				if (pipescount >= 90) {
					pipescount = 0;
					float r = rand() % 300;
					pip.setPosition(500.f, 625.f - r);
					rpip.setPosition(578.f, pip.getPosition().y-250);
					pipes.push_back(make_pair(pip, rpip));
				}
				v += gravity;
			}
		}

		if (bird.getPosition().y +46>= base.getPosition().y || bird.getPosition().y <=0) {
			overr = true;
			v=0;
		}
		bird.move(0, v);

		//Rotation
		if (!main && !overr) {
			if (j) {
				a = -20;
				bird.setRotation(a);
			}
			else if (a < 20.f) {
				a++;
				bird.setRotation(a);
			}
			for (auto &i : pipes) {
				i.first.move(-3, 0);
				i.second.move(-3, 0);
			}
			for (auto i : pipes) {
				if (i.first.getGlobalBounds().intersects(bird.getGlobalBounds())) { 
					overr = true; 
					v = 0;
				}
				if (i.second.getGlobalBounds().intersects(bird.getGlobalBounds())) { 
					overr = true;
					v = 0;
				}
				if (i.second.getPosition().x <= bird.getPosition().x && i.second.getPosition().x >= bird.getPosition().x - 3) {
					score++;
					s.setString(to_string(score));
				}
			}
		}
		if (overr && Keyboard::isKeyPressed(Keyboard::Space)) {
			overr = false;
			pipes.clear();
			main = true;
			bird.setPosition(window.getSize().x / 2 - 250 * 0.09, window.getSize().y / 2 - 170 * 0.09);
			a=0;
			bird.setRotation(a);
			keytime = 0;
		}

		//Draw
		window.clear();
		window.draw(background);

		if (main) {
			window.draw(title);
			window.draw(tap);
		}
		else if (overr) {
			for (auto i : pipes) {
				window.draw(i.first);
				window.draw(i.second);
			}
			window.draw(over);
			window.draw(s);
		}
		else {
			for (auto i : pipes) {
				window.draw(i.first);
				window.draw(i.second);
				window.draw(pip);
			}
			window.draw(s);
		}

		window.draw(bird);
		window.draw(base);
		window.display();
	}
	return 0;
}