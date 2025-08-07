"""
Giveaway model.
"""

import datetime

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from obearon.database.engine import Base


class Giveaway(Base):
    """
    Table that stores the giveaway.
    """

    __tablename__ = "giveaway"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    hoster_discord_id: Mapped[int] = mapped_column(BigInteger)
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    participants: Mapped[list["GiveawayParticipant"]] = relationship("GiveawayParticipant", back_populates="giveaway")
    winners: Mapped[list["GiveawayWinner"]] = relationship("GiveawayWinner", back_populates="giveaway")


class GiveawayParticipant(Base):
    """
    Table that stores the giveaway participants.
    """

    __tablename__ = "giveaway_participant"

    giveaway_id: Mapped[int] = mapped_column(ForeignKey("giveaway.id"), primary_key=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    giveaway: Mapped["Giveaway"] = relationship("Giveaway", back_populates="participants")


class GiveawayWinner(Base):
    """
    Table that stores the giveaway winners.
    """

    __tablename__ = "giveaway_winner"

    giveaway_id: Mapped[int] = mapped_column(ForeignKey("giveaway.id"), primary_key=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    giveaway: Mapped["Giveaway"] = relationship("Giveaway", back_populates="winners")
